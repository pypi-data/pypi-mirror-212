#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import sys
from abc import ABCMeta, abstractmethod
from .connector.maxcompute import MaxComputeConnector
from .util.logger import get_logger
from .util.table_info import TableInfo
from typing import List
from pydash import merge, _

logger = get_logger(__file__)


class MapReduceLauncherCheckException(Exception):
    pass


class MapReduceLauncher(metaclass=ABCMeta):
    """
    此类用于在python代码中执行mr，执行原理如下:

    调用拓扑: python(本文件) --sys-> java执行jar包 --ODPS sdk-> java mr

    路径变量定义:
    - mr_jar_base_path: 表示jar包所在位置(jar包中即包含mr代码，又包含命令行启动调用mr的代码)
    - project_base_path: python代码所在位置

    jar包同步: 在线上环境: 打包好的jar跟python文件在同一个base目录中， 即 project_base_path = mr_jar_base_path。
              在本地开发环境: jar包往往跟python不在同一目录下，所以会进行一步 jar 包拷贝，见函数 __copy_mr_jar
    """
    project_base_path: str
    mr_jar_base_path: str

    def __init__(self):
        # self.initialize()
        self.odps_conf_file_name: str
        self.mapper_class: str
        self.reducer_class: str
        self.mapper_key: str
        self.mapper_value: str
        self.input_table_list: List[str]
        self.output_table_list: List[str]
        self.table_resource_list: List[str]
        self.maxcompute_ins: MaxComputeConnector
        self.mr_jar_name: str
        self.mr_jar_resource_name: str
        self.ddl_file_path: str
        self.extend_parameters: dict = {}
        self.system_parameters: dict = {}
        self.init_parameters: dict = {}
        pass

    def initialize(self):
        self.mr_jar_base_path = self.init_mr_jar_base_path()
        self.project_base_path = self.init_project_base_path()
        self.odps_conf_file_name = self.init_odps_conf_file_name()

        self.mapper_class = self.init_mapper_class()
        self.reducer_class = self.init_reducer_class()
        self.mapper_key = self.init_mapper_key()
        self.mapper_value = self.init_mapper_value()
        self.input_table_list: List[TableInfo] = self.__normalize_table_info(
            self.init_input_table_with_partition_list()
        )
        self.output_table_list: List[TableInfo] = self.__normalize_table_info(
            self.init_output_table_with_partition_list()
        )
        self.table_resource_list: List[TableInfo] = self.__normalize_table_info(
            self.init_table_resource_list()
        )
        self.maxcompute_ins = self.init_maxcompute_ins()
        if 'maxcompute_ins' in self.init_parameters:
            self.__update_maxcompute_ins(self.init_parameters['maxcompute_ins'])
        if 'odps_ins' in self.init_parameters:
            self.__update_maxcompute_ins(self.init_parameters['odps_ins'])
        self.maxcompute_ins.save_odps_ini_file(os.path.join(self.project_base_path, self.odps_conf_file_name))

        self.mr_jar_name = self.init_mr_jar_name()
        self.mr_jar_resource_name = self.init_mr_jar_resource_name()
        self.ddl_file_path = self.init_ddl_file_path()
        self.extend_parameters = merge(self.__normalize_parameters(self.init_extend_parameters()), self.extend_parameters)
        self.system_parameters = merge(self.__normalize_parameters(self.init_system_parameters()), self.system_parameters)
        self.init_parameters = merge(self.__normalize_parameters(self.get_init_parameters()), self.init_parameters)

    def __update_maxcompute_ins(self, maxcompute_ins):
        self.maxcompute_ins = maxcompute_ins
        self.odps_conf_file_name = 'odps_' + self.maxcompute_ins.project + '.ini'
        pass

    @staticmethod
    def __check_partition_of_table_list(list_table: List[TableInfo]):
        """
        确保table_info_list的表是分区表排在前面的
        :type list_table: tableInfo
        :return:
        """
        if len(list_table) > 1:
            filtered_list = list(filter(
                lambda x: x.get_partition() is not None,
                list_table
            ))
            if len(filtered_list) != len(list_table):
                for i in range(len(filtered_list)):
                    if list_table[i].get_partition() is None:
                        raise MapReduceLauncherCheckException('有多个输入或者输出时，分区表需要排在前面，以便设置分区: 将以下表顺序延后 `{table_name}`'.format(
                            table_name=list_table[i].get_table_name_with_project()
                        ))
                    pass
                pass
            pass
        pass

    def set_init_parameter(self, key, val):
        self.init_parameters[key] = val

    def set_init_parameters(self, map_key_val):
        for key in map_key_val:
            self.init_parameters[key] = map_key_val[key]

    @staticmethod
    def get_init_parameters():
        return {}

    def set_extend_parameter(self, key, val):
        self.extend_parameters[key] = val

    def set_extend_parameters(self, map_key_val):
        for key in map_key_val:
            self.extend_parameters[key] = map_key_val[key]

    def set_system_parameter(self, key, val):
        self.system_parameters[key] = val

    def set_system_parameters(self, map_key_val):
        for key in map_key_val:
            self.system_parameters[key] = map_key_val[key]

    @abstractmethod
    def init_mr_jar_base_path(self, mr_jar_base_path: str = None):
        return mr_jar_base_path

    @abstractmethod
    def init_project_base_path(self, mr_jar_base_path: str = None):
        return mr_jar_base_path

    @staticmethod
    def init_odps_conf_file_name(init_odps_conf_file_name: str = 'odps_ali_conf.ini'):
        return init_odps_conf_file_name

    @abstractmethod
    def init_mapper_class(self, mapper_class: str = None):
        return mapper_class

    @abstractmethod
    def init_reducer_class(self, reducer_class: str = None):
        return reducer_class

    def init_input_table_with_partition_list(self):
        """
        :param table_name_with_partition_list: [[table_name, partition]...]
        :return:
        """
        if type(self.init_parameters['input_table']) == list:
            return self.init_parameters['input_table']
        else:
            return [
                self.init_parameters['input_table']
            ]

    @abstractmethod
    def init_mapper_key(self, mapper_key: str = None):
        return mapper_key

    @abstractmethod
    def init_mapper_value(self, mapper_value: str = None):
        return mapper_value

    def init_output_table_with_partition_list(self):
        """
        :param table_name_with_partition_list: [[table_name, partition]...]
        :return:
        """
        if type(self.init_parameters['output_table']) == list:
            return self.init_parameters['output_table']
        else:
            return [
                self.init_parameters['output_table']
            ]

    def init_table_resource_list(self):
        """
        表资源
        :param table_resource_list: [[table_name, partition, resource_name],...]
        :return: 可以为空
        """
        if 'resource_table' not in self.init_parameters:
            return []

        if type(self.init_parameters['resource_table']) == list:
            return self.init_parameters['resource_table']
        else:
            return [
                _.get(self.init_parameters, 'resource_table', None)
            ]

    @abstractmethod
    def init_maxcompute_ins(self, maxcompute_ins: MaxComputeConnector = None):
        return maxcompute_ins

    @abstractmethod
    def init_mr_jar_name(self, mr_jar_name: str = None):
        return mr_jar_name

    @abstractmethod
    def init_extend_parameters(self, extend_parameters: dict = None):
        """
        :param extend_parameters: {key: value}
        :return: 可以为空
        """
        return extend_parameters

    @abstractmethod
    def init_system_parameters(self, system_parameters: dict = None):
        """
        只控制 下面这三个参数，默认值如下
          -splitSize 32
          -reduceCnt 100
          -reduceMem 4096
        :param system_parameters: {'splitSize': '16', 'resuceCnt': '900', 'reduceMem': 4096}
        :return: 可以为空
        """
        pass

    @staticmethod
    def __normalize_parameters(parameters: dict):
        if not parameters:
            return {}
        else:
            return parameters

    @abstractmethod
    def init_ddl_file_path(self, ddl_file_path: str = None):
        return ''

    @staticmethod
    def init_mr_jar_resource_name():
        return ''

    def __upload_mr_jar_resource(self):
        self.mr_jar_resource_name = self.maxcompute_ins.update_mr_jar(
            self.mr_jar_base_path,
            self.project_base_path,
            mr_jar_name=self.mr_jar_name,
            resource_name=self.mr_jar_resource_name,
        )

    def __upload_table_resource(self):
        if not self.table_resource_list:
            return

        for resource_table in self.table_resource_list:
            if self.maxcompute_ins.exist_resource(resource_table.get_resource_name()):
                self.maxcompute_ins.delete_resource(resource_table.get_resource_name())
            self.maxcompute_ins.create_resource(
                resource_table.get_resource_name(),
                'table',
                table_name=resource_table.get_table_name_with_project(),
                partition=resource_table.get_partition(),
                # project=resource_table.get_project()      # 注册资源只准注册在本 odps_ins 的 project
            )
        pass

    @staticmethod
    def __normalize_table_info(table_list):
        if not isinstance(table_list, List):
            table_list = [table_list]

        table_list = list(filter(
            lambda x: x is not None,
            table_list
        ))
        for idx, table_info in enumerate(table_list):
            if not isinstance(table_info, TableInfo):
                if isinstance(table_info, str):
                    table_list[idx] = TableInfo(table_info)
                elif isinstance(table_info, List):
                    table_list[idx] = TableInfo(
                        _.get(table_info, '0'),
                        partition=_.get(table_info, '1'),
                        resource_name=_.get(table_info, '2'),
                    )
                pass
            pass

        return table_list

    def __delete_output_partition(self):
        for output_table_info in self.output_table_list:
            table_ins = self.maxcompute_ins.get_table(output_table_info.get_table_name(), project=output_table_info.get_project())
            if output_table_info.get_partition() is not None:
                table_ins.delete_partition(partition_spec=output_table_info.get_partition(), if_exists=True)
            else:
                table_ins.truncate()
            pass
        pass

    def __run_sql_in_file(self):
        if self.ddl_file_path:
            self.maxcompute_ins.run_sql_in_file(self.ddl_file_path, self.init_parameters)
        pass

    def __get_proxy_prefix(self):
        if self.maxcompute_ins.rest._proxy is None:
            return ''

        proxy_info = self.maxcompute_ins.rest._proxy['http']
        if proxy_info.startswith('socks5://'):
            host_port = proxy_info.split('://')[1].split(':')
            return f' -DsocksProxyHost={host_port[0]} -DsocksProxyPort={host_port[1]} '
        else:
            raise Exception(f'proxy type {proxy_info} not supported!')
        pass

    def __execute_mr(self):
        cmd = '''
          java {proxy_prefix} -Djava.ext.dirs={project_base_path}/target/lib -cp
            target/{mr_jar_name}
            com.aliyun.citybrain.traffic.MapReduceLauncher
          -odps_conf_file_name  {odps_conf_file_name}
          -project_base_path {project_base_path}
          -mapper {mapper_class}
          -reducer {reducer_class}
          -key {mapper_key}
          -value {mapper_value}
          -input {input_table_name}
          -partin {input_table_partition}
          -output {output_table_name}
          -partout {output_table_partition}
          -resource {mr_jar_resource_name} {table_resource}
          {extend_parameters}
          -splitSize {system_parameters_split_size}
          -reduceCnt {system_parameters_reduce_cnt}
          -reduceMem {system_parameters_reduce_mem}
        '''.format(
            proxy_prefix=self.__get_proxy_prefix(),
            odps_conf_file_name=self.odps_conf_file_name,
            mr_jar_resource_name=self.mr_jar_resource_name,
            mr_jar_name=self.mr_jar_name, project_base_path=self.project_base_path,
            mapper_class=self.mapper_class, reducer_class=self.reducer_class,
            mapper_key=self.mapper_key, mapper_value=self.mapper_value,
            input_table_name=' '.join(list(map(
                lambda x: x.get_table_name_with_project(),
                self.input_table_list
            ))),
            input_table_partition=' '.join(list(map(
                lambda x: x.get_partition(),
                list(filter(
                    lambda t: t.get_partition() is not None,
                    self.input_table_list
                ))
            ))),
            output_table_name=' '.join(list(map(
                lambda x: x.get_table_name_with_project(),
                self.output_table_list
            ))),
            output_table_partition=' '.join(list(map(
                lambda x: x.get_partition(),
                list(filter(
                    lambda t: t.get_partition() is not None,
                    self.output_table_list
                ))
            ))),
            table_resource=' '.join(list(map(
                lambda x: x.get_resource_name(),
                self.table_resource_list
            ))),
            extend_parameters=' '.join(list(map(
                lambda x: '-' + x + ' ' + str(self.extend_parameters[x]),
                self.extend_parameters.keys()
            ))),
            system_parameters_split_size=self.system_parameters['splitSize']
            if 'splitSize' in self.system_parameters else '32',
            system_parameters_reduce_cnt=self.system_parameters['reduceCnt']
            if 'reduceCnt' in self.system_parameters else '100',
            system_parameters_reduce_mem=self.system_parameters['reduceMem']
            if 'reduceMem' in self.system_parameters else '4096'
        ).replace('\n', '\\\n').replace('$', '\$')

        logger.info(cmd)
        cmd_exit_code = os.system(cmd)
        logger.info('cmd_exit_code => ' + str(cmd_exit_code))
        if cmd_exit_code != 0:
            sys.exit()
        pass

    def launch(self):
        self.initialize()
        self.__run_sql_in_file()
        self.__upload_mr_jar_resource()
        self.__upload_table_resource()
        self.__delete_output_partition()
        self.__execute_mr()
        pass
