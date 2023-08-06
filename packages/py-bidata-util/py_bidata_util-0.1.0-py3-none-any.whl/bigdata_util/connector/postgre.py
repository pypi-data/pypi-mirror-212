#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from bigdata_util.connector.base_query import IBaseQuery
from bigdata_util.util import get_logger
from bigdata_util.util import lnglat_seq_2_wkt, safe_get_and_not_none
from typing import List
import os
import select
import odps

logger = get_logger(__name__)


class PostgreConnector(IBaseQuery):
    enable = False

    # "host=localhost dbname=postgres user=postgres password= port=5432"
    def __init__(self, conn_info):
        if conn_info:
            import psycopg2
            if conn_info.startswith('postgresql'):
                from urllib.parse import urlparse, parse_qs
                r = urlparse(conn_info)
                qs = parse_qs(r.query)
                password = r.password
                if 'password' in qs:
                    password = qs['password'][0]
                dbname = r.path[1:]
                conn_info = f'host={r.hostname} dbname={dbname} user={r.username} password={password}'
                if r.port is not None:
                    conn_info +=  f' port={r.port}'
            self.__conn = psycopg2.connect(
                conn_info,
                async_=1,
                keepalives=1, # 保持连接
                keepalives_idle=130, # 空闲时，每130秒保持连接连通
                keepalives_interval=10, # 没得到回应时，等待10秒重新尝试保持连通
                keepalives_count=15 # 尝试最多15次重新保持连通
            )
            self.wait(self.__conn)
            self.enable = True
        else:
            self.__conn = None
        pass

    @staticmethod
    def wait(conn):
        import psycopg2
        while True:
            state = conn.poll()
            if state == psycopg2.extensions.POLL_OK:
                break
            elif state == psycopg2.extensions.POLL_WRITE:
                select.select([], [conn.fileno()], [])
            elif state == psycopg2.extensions.POLL_READ:
                select.select([conn.fileno()], [], [])
            else:
                raise psycopg2.OperationalError("poll() returned %s" % state)

    def __del__(self):
        if self.__conn is not None:
            try:
                self.__conn.close()
            except Exception as e:
                pass
        pass

    def __check_enable(self):
        return self.enable

    def execute_sql(self, sql, sql_hints=None, show_log=False):
        if 'DEBUG_PY_BIGDATA_UTIL' in os.environ or show_log:
            logger.info(f'''
executing sql: >>> {sql} <<<
''')
        return self.execute_without_result(sql)

    def run_sql_without_result(self, sql):
        self.execute_without_result(sql)

    def execute_without_result(self, sql):
        if not self.__check_enable():
            return

        cur = self.__conn.cursor()
        try:
            cur.execute(sql)
            self.wait(cur.connection)
        except Exception as e:
            logger.error('Error occurred when executing:')
            logger.error(sql)
            raise e
        finally:
            cur.close()

        # self.__conn.commit()

    def description(self, table_name):
        if not self.__check_enable():
            return
        schema_name = 'public'
        table_name_with_schema = table_name.split('.')
        if len(table_name_with_schema) > 1:
            schema_name = table_name_with_schema[0]
            table_name = table_name_with_schema[1]

        # cur.execute('select * from {tableName} limit 1'.format(tableName=tableName))
        column_list = self.run_sql_return_plain_json(f'''
SELECT
    -- a.attnum,
    d.nspname,
    a.attname AS column_name,
    t.typname AS data_type,
    -- a.attlen AS length,
    -- a.atttypmod AS lengthvar,
    not a.attnotnull AS is_nullable,
    b.description AS comment
FROM pg_class c join pg_namespace d on (c.relnamespace = d.oid)
, pg_attribute a
    LEFT JOIN pg_description b
    ON a.attrelid = b.objoid
        AND a.attnum = b.objsubid, pg_type t
WHERE c.relname = '{table_name.lower()}' and d.nspname = '{schema_name.lower()}'
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
WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = '{table_name.lower()}' and tc.table_schema = '{schema_name.lower()}';
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

    def executemany(self, sql, namedict):
        if not self.__check_enable():
            return
        logger.info(f'''
        executing sql: >>> {sql} <<<
        ''')

        cur = self.__conn.cursor()
        cur.executemany(sql, namedict)
        self.wait(cur.connection)
        cur.close()
        pass

    def execute_without_result_without_commit(self, sql):
        if not self.__check_enable():
            return
        logger.info(f'''
        executing sql: >>> {sql} <<<
        ''')

        cur = self.__conn.cursor()
        cur.execute(sql)
        self.wait(cur.connection)
        cur.close()

    def execute_with_result(self, sql, show_log=True):
        if not self.__check_enable():
            return

        if 'DEBUG_PY_BIGDATA_UTIL' in os.environ or show_log:
            logger.info(f'''
executing sql: >>> {sql} <<<
''')

        cur = self.__conn.cursor()
        cur.execute(sql)
        self.wait(cur.connection)
        fetched_list = cur.fetchall()
        cur.close()

        return cur, fetched_list

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
        if not self.__check_enable():
            return

        self.execute_without_result('drop table if exists ' + table_name + ';')
        pass

    def __update_geometry_collection_empty(self, table_name, col_name_wkt, geometry_type):
        sql = '''
            update {table_name} set {col_name_wkt} = \'{geometry_type} EMPTY\'
            where {col_name_wkt} = \'GEOMETRYCOLLECTION EMPTY\';
        '''.format(
            table_name=table_name,
            col_name_wkt=col_name_wkt,
            geometry_type=geometry_type.upper(),
        )
        logger.info(sql)
        self.execute_without_result(sql)
        pass

    def gen_geom_col(self, table_name, col_name_wkt, col_name_geom, geometry_type):
        if not self.__check_enable():
            return
        self.__update_geometry_collection_empty(table_name, col_name_wkt, geometry_type)

        alter_sql = 'alter table {} add column {} geometry({},4326);'.format(table_name, col_name_geom, geometry_type)
        logger.info(alter_sql)
        self.execute_without_result(alter_sql)
        update_sql = 'update {} set {} = st_geometryfromtext({},4326);'.format(table_name, col_name_geom, col_name_wkt)
        logger.info(update_sql)
        self.execute_without_result(update_sql)
        pass

    def create_table_and_save_data(self, table_name, data_list, ignore_cols=[], pick_cols=[]):
        if not self.__check_enable():
            return

        first_item = data_list[0]
        self.create_table(list(map(
            lambda x: [x, 'varchar'],
            first_item.keys()
        )), table_name, force=True, ignore_cols=ignore_cols, pick_cols=pick_cols)

        self.save_data(table_name, data_list, ignore_cols=ignore_cols, pick_cols=pick_cols)
        pass

    def save_data(self, table_name, data_list, batch_size=10000, show_log=False, file_writer=None, ignore_cols=[], pick_cols=[]):
        if not self.__check_enable():
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
                self.execute_without_result(sql)

            batch_n += 1
            pass
        logger.info('saved to table "%s" total records: %d' % (table_name, len(data_list)))
        pass

    def save_geometry_table(self, table_name: str, list_data: List[dict],
                            col_name_geom='lnglat_seq', col_name_wkt='wkt', geometry_type='geometry', ignore_cols=[], geom_col_name='_geom_', batch_size=10000):
        if len(list_data) < 1:
            logger.warning('list data is empty.')
            return

        if isinstance(list_data[0], odps.models.Record):
            keys = list(map(
                lambda x: x.name,
                list_data[0].__getattribute__('_columns'))
            )
            new_data = []
            for row in list_data:
                meta = {}
                for key in keys:
                    meta[key] = safe_get_and_not_none(row, key)
                new_data.append(meta)
            list_data = new_data
        else:
            keys: List[str] = list(list_data[0].keys())

        if col_name_wkt not in keys:
            keys.append(col_name_wkt)

        keys = list(filter(
            lambda x: x not in ignore_cols,
            keys
        ))

        self.create_table(list(map(
            lambda x: [x, 'varchar'],
            keys
        )), table_name, force=True)

        for d in list_data:
            if col_name_wkt not in d or d[col_name_wkt] is None:
                d[col_name_wkt] = lnglat_seq_2_wkt(safe_get_and_not_none(d, col_name_geom, ''), geometry_type)

        self.save_data(table_name, list_data, batch_size=batch_size)
        self.gen_geom_col(table_name, col_name_wkt, geom_col_name, geometry_type)
        pass

    def run_sql_return_plain_json(self, sql, show_log=True):
        if not self.__check_enable():
            return []
        result = []

        cur, fetched_list = self.execute_with_result(sql, show_log=show_log)
        if cur.description is None or len(cur.description) < 1:
            return result

        for row in fetched_list:
            meta = {}
            for col, val in zip(cur.description, row):
                meta[col.name] = val
            result.append(meta)

        return result

    def run_sql_with_logview_return_plain_json(self, sql):
        return self.run_sql_return_plain_json(sql)

PostGreConnector = PostgreConnector
