#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from abc import ABCMeta, abstractmethod
import re


class IBaseQuery(metaclass=ABCMeta):
    @abstractmethod
    def run_sql_return_plain_json(self, sql):
        pass

    @abstractmethod
    def create_table(self, schema_or_desc, table_name, force=False):
        pass

    @abstractmethod
    def execute_sql(self, sql, sql_hints=None, show_log=False):
        pass

    @abstractmethod
    def exist_table(self, table_name):
        pass

    @abstractmethod
    def run_sql_with_logview_return_plain_json(self, sql):
        pass

    def execute_sql_auto_slim(self, sql, sql_hints=None, show_log=False):
        sql = self.slim_sql(sql)

        if sql == '':
            return

        return self.execute_sql(sql, sql_hints, show_log)

    def slim_sql(self, original_sql):
        sql = original_sql.strip()
        sql_part = sql.split('\n')

        sql = '\n'.join(list(filter(
            lambda x: x and not x.startswith('--'),
            sql_part
        )))

        return sql

    def run_sql_in_file(self, file_name, placeholder_value_map=None, sql_hints=None):
        """
        run sql in maxcompute file, support placeholder values.
        :param sql_hints:
        :param file_name:
        :param placeholder_value_map:
        :return:
        """
        if placeholder_value_map is None:
            placeholder_value_map = {}
        if sql_hints is None:
            sql_hints = {}
        with open(file_name, mode='rb') as reader:
            sql_list_str = reader.read().decode('utf-8')
            sql_list_str = self.replace_placeholder_values(sql_list_str, placeholder_value_map)

            sql_list = re.split(';[$\n]', sql_list_str)
            for sql in sql_list:
                if sql is not None and sql is not '':
                    self.execute_sql_auto_slim(sql, sql_hints=sql_hints)
                pass
            pass
        pass

    @staticmethod
    def replace_placeholder_values(original_sql: str, value_map: dict) -> str:
        result_sql = original_sql

        if value_map is None:
            return result_sql

        pattern = re.compile(r'\${.*?}')
        placeholder_value_map = {}
        for key in pattern.findall(result_sql):
            key_in_map = key[2:-1].split('.')[0]
            if key_in_map not in value_map:
                continue
            placeholder_value_map[key] = key[1:].format(**value_map)

        for key in placeholder_value_map.keys():
            result_sql = result_sql.replace(key, str(placeholder_value_map[key]))
            pass

        return result_sql

