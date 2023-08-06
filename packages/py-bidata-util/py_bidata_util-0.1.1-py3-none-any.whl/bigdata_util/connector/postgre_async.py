#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from bigdata_util.connector.base_query import IBaseQuery
from bigdata_util.util import get_logger, set_proxy_global, reset_proxy_global, get_event_loop
import os
import sys
import json

logger = get_logger(__name__)


class PostgreAsyncConnector(IBaseQuery):
    def __init__(self, conn_info, proxy=None):
        self.conn_info = conn_info
        self.proxy = proxy
        self.enable = False
        self.active = False
        self.proxy_active = False
        self.conn = None

        if conn_info:
            import asyncpg
            self.enable = True
            if proxy is not None:
                self.__check_enable_and_active_proxy()
            self.conn = get_event_loop().run_until_complete(asyncpg.connect(conn_info))
            self.__dismiss_proxy()
        else:
            self.conn = None
        pass

    def __check_enable(self):
        return self.enable

    def __del__(self):
        if self.proxy is not None:
            self.__check_enable_and_active_proxy()

        if self.conn is not None and not self.conn.is_closed():
            try:
                # do nothing
                pass
                # self.conn.close()
                # get_event_loop().run_until_complete()
            except Exception as e:
                pass

        # get_event_loop().close()

        # 由于这个函数是随机被调用的，并不是析构函数；由于__dismiss_proxy在执行完成后基本都会被调用这里不需要重复调用了。
        # self.__dismiss_proxy()
        pass

    def __check_enable_and_active_proxy(self):
        if not self.enable:
            return False

        if self.proxy is None:
            return True

        if not self.proxy_active:
            set_proxy_global(self.proxy)
            self.proxy_active = True

        return True

    def __dismiss_proxy(self):
        if self.proxy_active:
            reset_proxy_global()
            self.proxy_active = False
        pass

    def execute_sql(self, original_sql, sql_hints=None, param_map=None, return_type=None, show_log=False):
        result = None
        if not self.__check_enable_and_active_proxy():
            return result

        final_sql = self.replace_placeholder_values(original_sql, param_map)

        if 'DEBUG_PY_BIGDATA_UTIL' in os.environ or show_log:
            logger.info(f'''
executing sql: >>> {final_sql} <<<
''')

        if return_type is None:
            get_event_loop().run_until_complete(self.conn.execute(
                final_sql
            ))
        elif return_type == 'records':
            result = get_event_loop().run_until_complete(self.conn.fetch(
                final_sql
            ))
        elif return_type == 'plain_json':
            result = self.__record_to_json(get_event_loop().run_until_complete(self.conn.fetch(
                final_sql
            )))

        self.__dismiss_proxy()
        return result

    def run_sql_return_plain_json(self, *args, **kwargs):
        return self.execute_sql(*args, **kwargs, return_type='plain_json')

    def __record_to_json(self, data_list):
        if len(data_list) == 0:
            return []

        key_list = list(data_list[0].keys())
        return list(map(lambda x: self.__gen_json_from_record(x, key_list), data_list))

    @staticmethod
    def __gen_json_from_record(r, k):
        meta = {}
        for col_name in k:
            meta[col_name] = r.get(col_name)
        return meta

    def run_sql_with_logview_return_plain_json(self, *args, **kwargs):
        return self.run_sql_return_plain_json(*args, **kwargs)

    def description(self, table_name):
        if not self.__check_enable_and_active_proxy():
            return

        # cur.execute('select * from {tableName} limit 1'.format(tableName=tableName))
        column_list = self.run_sql_return_plain_json(f'''
            SELECT
                -- a.attnum,
                a.attname AS column_name,
                t.typname AS data_type,
                -- a.attlen AS length,
                -- a.atttypmod AS lengthvar,
                not a.attnotnull AS is_nullable,
                b.description AS comment
            FROM pg_class c, pg_attribute a
                LEFT JOIN pg_description b
                ON a.attrelid = b.objoid
                    AND a.attnum = b.objsubid, pg_type t
            WHERE c.relname = '{table_name.lower()}'
                AND a.attnum > 0
                AND a.attrelid = c.oid
                AND a.atttypid = t.oid
            ORDER BY a.attnum;
        ''', show_log=False)
        pk_list = self.run_sql_return_plain_json(f'''
            SELECT c.column_name, c.data_type
            FROM information_schema.table_constraints tc
            JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
            JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
              AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
            WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '{table_name.lower()}';
        ''', show_log=False)
        pk_col_name_map = {}
        for pk in pk_list:
            pk_col_name_map[pk['column_name']] = True

        for col in column_list:
            if col['column_name'] in pk_col_name_map:
                col['is_pk'] = True
            else:
                col['is_pk'] = False

        return column_list

    def exist_table(self, table_name):
        result = self.run_sql_return_plain_json(f'''
            SELECT EXISTS (
                SELECT FROM
                    pg_tables
                WHERE
                    schemaname = 'public' AND
                    tablename  = '{table_name}'
            ) as exist_table
        ''')
        return result[0]['exist_table']

    def create_table(self, table_schema, table_name, force=False, ignore_cols=[], pick_cols=[]):
        if not self.__check_enable():
            return

        if force:
            self.drop_table(table_name)

        sql = self.format_ddl(table_schema, table_name, ignore_cols=ignore_cols, pick_cols=pick_cols)
        self.execute_without_result(sql)
        pass

    @staticmethod
    def format_ddl(schema_or_desc, table_name, ignore_cols=[], pick_cols=[]):
        if not schema_or_desc or len(schema_or_desc) < 1:
            raise '创建表的schema为空'
        desc = schema_or_desc
        if isinstance(schema_or_desc[0], list):
            desc = list(map(
                lambda x: {
                    'column_name': x[0],
                    'data_type': x[1],
                    'is_nullable': True,
                    'is_pk': False
                },
                schema_or_desc
            ))
            pass

        if len(pick_cols) > 0:
            desc = list(filter(lambda x: x['column_name'] in pick_cols, desc))
        else:
            desc = list(filter(lambda x: x['column_name'] not in ignore_cols, desc))

        col_str_list = []
        pk_col_names = []
        partition_col_names = []
        for r in desc:
            column_name = r['column_name']
            data_type = r['data_type']
            r_str = f' {column_name} {data_type} '
            if 'is_nullable' in r and not r['is_nullable']:
                r_str += ' not null'
            if 'is_pk' in r and r['is_pk']:
                pk_col_names.append(column_name)
            if 'is_partition' in r and r['is_partition']:
                partition_col_names.append(column_name)
            col_str_list.append(r_str)
            pass

        if len(pk_col_names) > 0:
            pk_col_name_str = ', '.join(pk_col_names)
            col_str_list.append(f'CONSTRAINT {table_name}_pk PRIMARY KEY ({pk_col_name_str})')

        col_str = ',\n'.join(col_str_list)

        if len(partition_col_names) > 0:
            partition_col_str = ', '.join(partition_col_names)
            suffix = f'partition by list ({partition_col_str})'
        else:
            suffix = ''

        return f'''
            create table if not exists {table_name} (
                {col_str}
            ) {suffix}
        '''

    def drop_table(self, table_name):
        if not self.__check_enable_and_active_proxy():
            return

        self.execute_sql('drop table if exists ' + table_name + ';')

    def save_data(self, table_name, data_list, batch_size=10000, show_log=False, file_writer=None, ignore_cols=[], pick_cols=[]):
        if not self.__check_enable_and_active_proxy():
            return

        desc = self.description(table_name)
        if len(pick_cols) > 0:
            desc = list(filter(lambda x: x['column_name'] in pick_cols, desc))
        else:
            desc = list(filter(lambda x: x['column_name'] not in ignore_cols, desc))

        names = list(map(
            lambda x: x['column_name'],
            desc
        ))

        # 主键自动更新
        pk_conflict_update_addon = ''
        pk_list = list(filter(lambda x: x['is_pk'], desc))
        pk_name_list = list(map(lambda x: x['column_name'], pk_list))
        normal_col_list = list(filter(lambda x: not x['is_pk'], desc))
        normal_col_name_list = list(map(lambda x: x['column_name'], normal_col_list))
        if len(pk_list) > 0:
            pk_names = ', '.join(pk_name_list)

            pk_conflict_update_addon = f'''
                ON CONFLICT ({pk_names})
            '''
            pass

        if len(normal_col_name_list) > 0:
            col_set_list = list(map(
                lambda x: f"{x} = excluded.{x}",
                normal_col_name_list
            ))
            col_set = ',\n'.join(col_set_list)
            pk_conflict_update_addon += f'''
                DO UPDATE
                    SET {col_set}
            '''
        else:
            pk_conflict_update_addon += f'''
                DO NOTHING
            '''

        logger.info('saving to table "%s" total records: %d' % (table_name, len(data_list)))

        # save with batch_size
        batch_n = 0
        while batch_n * batch_size < len(data_list):
            logger.info('saved %d.' % (batch_n * batch_size))
            base_sql = 'insert into {}('.format(table_name) + ','.join(names) + ') values'

            row_values = []
            for meta in data_list[batch_n * batch_size : (batch_n + 1) * batch_size]:
                values = []
                for col in desc:
                    if col['column_name'] in meta:
                        val = meta[col['column_name']]
                    else:
                        val = None
                    if col['data_type'].startswith('character') or col['data_type'].startswith('text') or col['data_type'].startswith('varchar'):
                        if val is None:
                            values.append('null')
                        else:
                            values.append("'{}'".format(str(val).replace("'", "''")))
                    elif col['data_type'].startswith('geometry'):
                        if val is None:
                            values.append('null')
                        else:
                            values.append(f"ST_GeomFromWKB(decode('{val}', 'hex'))")
                    else:
                        if val is None:
                            values.append('null')
                        else:
                            values.append("{}".format(val))
                    pass
                row_values.append('(' + ','.join(values) + ')')
            sql = base_sql + ', '.join(row_values)

            if len(pk_list) > 0:
                sql += pk_conflict_update_addon

            if file_writer is not None:
                file_writer.write((sql + ';\n').encode('utf-8'))
            else:
                self.execute_sql(sql, show_log=show_log)

            batch_n += 1
            pass
        logger.info('saved to table "%s" total records: %d' % (table_name, len(data_list)))
        pass

    def execute_without_result(self, *args, **kwargs):
        return self.execute_sql(*args, **kwargs)
  
