#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from bigdata_util.connector.base_query import IBaseQuery
from bigdata_util.util import get_logger, set_proxy_global, reset_proxy_global
import os
import sys
import json

logger = get_logger(__name__)


class MysqlConnector(IBaseQuery):
    enable = False

    def __init__(self, *args, proxy=None, **kwargs):
        import pymysql
        self.proxy = proxy
        self.__conn = pymysql.connect(*args, **kwargs, defer_connect=True)
        self.enable = True
        self.proxy_active = False

        # TODO: PyMysql支持传入sock对象，后续可以升级为传入代理后sock对象，避免修改全局代理。
        self.enable_proxy()
        pass

    def __del__(self):
        self.__check_enable_and_active_proxy()

        if self.__conn is not None:
            self.__conn.close()

        self.__dismiss_proxy()
        pass

    def create_table(self, schema_or_desc, table_name):
        # TODO
        pass

    def exist_table(self, table_name):
        # TODO
        pass

    def enable_proxy(self):
        self.__check_enable_and_active_proxy()
        self.__conn.connect()
        self.__dismiss_proxy()
        pass

    def __check_enable_and_active_proxy(self):
        result = False

        if not self.enable:
            result = False

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

    def run_sql_return_plain_json(self, *args, **kwargs):
        return self.execute_sql(*args, **kwargs, return_type='plain_json')

    def execute_sql(self, original_sql, sql_hints=None, param_map=None, return_type=None, show_log=False):
        result = None
        if not self.__check_enable_and_active_proxy():
            return result

        final_sql = self.replace_placeholder_values(original_sql, param_map)

        if 'DEBUG_PY_BIGDATA_UTIL' in os.environ or show_log:
            logger.info(f'''
            executing sql: >>> {final_sql} <<<
            ''')

        cursor = self.__conn.cursor()
        if return_type is None:
            cursor.execute(final_sql)
        elif return_type == 'records':
            result = cursor.fetchall(cursor.execute(final_sql))
        elif return_type == 'plain_json':
            cursor.execute(final_sql)
            result = self.__record_to_json(
                cursor.description,
                cursor.fetchall()
            )
        
        cursor.close()

        self.__dismiss_proxy()
        return result

    @staticmethod
    def __record_to_json(description, data_list):
        result = []

        if description is None or len(description) < 1:
            return result

        if data_list is None or len(data_list) < 1:
            return result

        key_list = list(map(lambda x: x[0], description))
        for row in data_list:
            meta = {}
            for key, val in zip(key_list, row):
                meta[key] = val

            result.append(meta)

        return result

    def run_sql_with_logview_return_plain_json(self, *args, **kwargs):
        return self.run_sql_return_plain_json(*args, **kwargs)


