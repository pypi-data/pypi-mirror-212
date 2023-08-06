#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from . import get_logger
from pyhocon import ConfigFactory, HOCONConverter, ConfigTree
import os
from configobj import ConfigObj
import pydash

logger = get_logger(__file__)


class BaseConfig(object):
    _config = None
    _needed_config_attr = []

    _config_file_path = 'config.conf'

    def get(self, name, default_value=''):
        return self._config.get(name, default_value)

    def put(self, name, value):
        return self._config.put(name, value)

    def __init__(self, config=None, config_file_path='config.conf'):
        """
        可以传入config，也可以从文件中读取
        :param config:
        :param config_file_path:
        """

        config_from_file = self.__load_config_from_file(config_file_path)
        if config_from_file is None:
            config_from_file = []
        config_from_parameter = ConfigFactory.from_dict(config)
        if config_from_parameter is None:
            config_from_parameter = []
        self._config_file_path = config_file_path
        self._config = ConfigTree.merge_configs(ConfigTree(config_from_file), ConfigTree(config_from_parameter))

        self._abs_config_file_path = os.path.abspath(self._config_file_path)
        self.__check_config()
        pass

    @staticmethod
    def __load_config_from_file(config_file_path):
        """
        从文件中load配置
        :param config_file_path:
        :return:
        """
        return ConfigFactory.parse_file(config_file_path, required=False)

    def __check_config(self):
        """
        检查config是否齐全，不齐全时，报错提示
        :return:
        """
        attr_temp_place_holder = 'TODO: <!- please add config here. ->'

        missing_config_attr = []
        append_to_file = []
        for config_attr in self._needed_config_attr:
            if config_attr not in self._config or self._config[config_attr] == attr_temp_place_holder:
                if config_attr not in self._config:
                    append_to_file.append('\n' + config_attr + ' = "' + attr_temp_place_holder + '"')
                # self._config.put(config_attr, attr_temp_place_holder)
                missing_config_attr.append('\n                    - "' + config_attr + '"')

        if len(missing_config_attr) > 0:
            if not os.path.isfile(self._config_file_path):
                with open(self._config_file_path, 'w') as writer:
                    if HOCONConverter.to_hocon(self._config) != '[]':
                        writer.write(HOCONConverter.to_hocon(self._config))
                    for line in append_to_file:
                        writer.write(line)
            elif len(append_to_file) > 0:
                with open(self._config_file_path, 'a') as writer:
                    for line in append_to_file:
                        writer.write(line)

            raise Exception('''
                Config needed, please edit "{config_file_path}" and fill needed config.
                
                Please open =====> "{abs_config_file_path}" <===== and fill needed config!!!
                
                missing configs: 
                {missing_config_keys}
            '''.format(config_file_path=self._config_file_path, abs_config_file_path=self._abs_config_file_path,
                       missing_config_keys=' ,'.join(missing_config_attr)))
        pass

    @staticmethod
    def save_odps_ini(odps_config, file_name):
        cfg = ConfigObj(encoding='utf8')
        cfg.filename = file_name
        for k in odps_config.keys():
            cfg[k] = odps_config[k]
        cfg['project_name'] = cfg['project']
        cfg['end_point'] = cfg['endpoint']
        try:
            cfg.write()
        except Exception as e:
            logger.error(e)
            pass
        pass
