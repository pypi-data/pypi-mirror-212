#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
from tablestore import OTSClient, OTSServiceError
from bigdata_util.util import load_csv, save_csv, get_logger
from pydash import _
logger = get_logger(__file__)


class TableStoreConnector(OTSClient):

    @staticmethod
    def is_tablestore_connector() -> bool:
        return True

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], dict):
            self.endpoint = _.get(args[0], 'endpoint', _.get(args[0], 'endPoint'))
            self.access_id = _.get(args[0], 'access_id', _.get(args[0], 'accessId'))
            self.access_key = _.get(args[0], 'access_key', _.get(args[0], 'accessKey'))
            self.instance = _.get(args[0], 'instance')
            super(TableStoreConnector, self).__init__(
                self.endpoint,
                self.access_id,
                self.access_key,
                self.instance
            )
        else:
            super(TableStoreConnector, self).__init__(*args, **kwargs)
        pass

    def create_table_by_odps(self, odps_instance, table_name: str, key_col_list, ots_table_name=None):
        """
        在odps中查看表结构并在ots中建立对应的表
        :return:
        """
        if ots_table_name is None:
            ots_table_name = table_name

        t = odps_instance.get_table(table_name)
        odps_name_type_map = {}
        for idx, name in enumerate(t.schema.names):
            odps_name_type_map[name] = t.schema.types[idx].name

        odps_ots_type_mapping = {
            'string': 'string',
            'bigint': 'integer',
            'double': 'double',
            'boolean': 'boolean',
            'binary': 'binary'
        }
        ots_name_type_map = {}
        for name in odps_name_type_map:
            ots_name_type_map[name] = odps_ots_type_mapping[odps_name_type_map[name]]
            pass

        schema_of_primary_key = []
        for key_name in key_col_list:
            schema_of_primary_key.append((key_name, ots_name_type_map[key_name].upper()))

        from tablestore import TableMeta, TableOptions, ReservedThroughput, CapacityUnit
        table_meta = TableMeta(ots_table_name, schema_of_primary_key)
        table_option = TableOptions(-1, 2)
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))

        try:
            # self.delete_table(ots_table_name)
            self.create_table(table_meta, table_option, reserved_throughput)
        except OTSServiceError as e:
            pass
