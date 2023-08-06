
#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from bigdata_util.connector.base_query import IBaseQuery
from bigdata_util.util import get_logger, set_proxy_global, reset_proxy_global, get_event_loop
import os
import sys
import json

logger = get_logger(__name__)


class ClickHouseConnector(IBaseQuery):
    def __init__(self, conn_info, proxy=None) -> None:
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

    def run_sql_return_plain_json(self, sql):
        pass

    def create_table(self, schema_or_desc, table_name, force=False):
        pass

    def execute_sql(self, sql, sql_hints=None, show_log=False):
        pass

    def exist_table(self, table_name):
        pass

    def run_sql_with_logview_return_plain_json(self, sql):
        pass
