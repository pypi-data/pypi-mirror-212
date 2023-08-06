#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import re
from .logger import get_logger

logger = get_logger(__file__)


def replace_placeholder_values(sql_template: str, kv: dict, place_holder=None):
    result_sql = sql_template

    if place_holder is not None:
        pattern = re.compile(place_holder)
    else:
        pattern = re.compile(r'\${.*?}')
    placeholder_value_map = {}
    for key in pattern.findall(result_sql):
        key_in_map = key[2:-1].split('.')[0]
        if key_in_map not in kv:
            continue
        placeholder_value_map[key] = key[1:].format(**kv)

    for key in placeholder_value_map.keys():
        result_sql = result_sql.replace(key, str(placeholder_value_map[key]))
        pass

    return result_sql


def replace_placeholder_in_file(in_file_name, out_file_name=None, placeholder_value_map=None, place_holder=None):
    if placeholder_value_map is None:
        placeholder_value_map = {}
    with open(in_file_name, mode='rb') as reader:
        sql_list_str = reader.read().decode('utf-8')
        sql_list_str = replace_placeholder_values(sql_list_str, placeholder_value_map, place_holder=place_holder)
        if out_file_name is None:
            logger.info(sql_list_str)
        else:
            with open(out_file_name, mode='wb') as writer:
                writer.write(sql_list_str)
