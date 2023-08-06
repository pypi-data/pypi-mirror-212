#!/usr/bin/env python3
# -*- coding=utf-8 -*-


def lnglat_seq_2_wkt_core(lnglat_list, should_be_ring=False, round_level=6, multi_point=False):
    """
    :param lnglat_list: 经纬度序列
    :param should_be_ring: 是否强制为环(首尾的经纬度相同，若不同，则在尾部插入一个跟起始经纬度相同的值)
    :return:
    """
    replaced_list = list(map(
        lambda x: x.replace(',', ' '),
        lnglat_list
    ))
    for idx, lnglat in enumerate(replaced_list):
        lnglat_split = lnglat.split(' ')
        replaced_list[idx] = ' '.join([str(round(float(lnglat_split[0]), round_level)), str(round(float(lnglat_split[1]), round_level))])

    if should_be_ring and replaced_list[0] != replaced_list[-1]:
        replaced_list.append(replaced_list[0])

    if multi_point:
        for idx, val in enumerate(replaced_list):
            replaced_list[idx] = '(' + val + ')'

    return ', '.join(replaced_list)


def lnglat_seq_2_wkt(lnglat_seq, wkt_type='LINESTRING'):
    wkt_type_upper = wkt_type.upper()
    if wkt_type_upper == 'GEOMETRY':
        wkt_type_upper = 'POLYGON'
    if not lnglat_seq:
        return wkt_type_upper + ' EMPTY'
    if wkt_type_upper == 'LINESTRING':
        return wkt_type_upper + ' (' + lnglat_seq_2_wkt_core(lnglat_seq.split(';')) + ')'
    elif wkt_type_upper == 'LINEARRING':
        lnglat_list = list(map(
            lambda x: x.replace(',', ' '),
            lnglat_seq.split(';')
        ))
        if lnglat_list[0] != lnglat_list[len(lnglat_list) - 1]:
            lnglat_list.append(lnglat_list[0])
        return wkt_type_upper + ' (' + lnglat_seq_2_wkt_core(lnglat_list) + ')'
    elif wkt_type_upper == 'POLYGON':
        lnglat_list = list(map(
            lambda x: x.replace(',', ' '),
            lnglat_seq.split(';')
        ))
        if len(lnglat_list) < 4:
            return wkt_type_upper + ' EMPTY'
        return wkt_type_upper + ' ((' + lnglat_seq_2_wkt_core(lnglat_list) + '))'
    elif wkt_type_upper == 'POINT':
        return wkt_type_upper + ' (' + lnglat_seq_2_wkt_core(lnglat_seq.split(';'), 8) + ')'
    elif wkt_type_upper == 'MULTIPOLYGON':
        return wkt_type_upper + '(' + ', '.join(list(map(
            lambda x: '((' + lnglat_seq_2_wkt_core(x.split(';'), True) + '))',
            lnglat_seq.split('#')
        ))) + ')'
    elif wkt_type_upper == 'MULTIPOINT':
        return wkt_type_upper + '(' + lnglat_seq_2_wkt_core(lnglat_seq.split(';'), multi_point=True) + ')'


def safe_get_and_not_none(dict_map: dict, key: str, default_value=''):
    if key not in dict_map or dict_map[key] is None:
        return default_value
    else:
        return dict_map[key]
    pass


def get_lnglat_seq(geom):
    from shapely.geometry.base import BaseGeometry
    geom: BaseGeometry = geom
    from shapely.geometry import Polygon, MultiPolygon
    if geom.is_empty:
        return ''

    result_list = []
    if geom.geom_type.upper() == 'POLYGON':
        geom: Polygon = geom
        one_list = []
        for coord in geom.exterior.coords:
            one_list.append(','.join([str(round(coord[0], 6)), str(round(coord[1], 6))]))
        result_list.append(';'.join(one_list))
    elif geom.geom_type.upper() == 'MULTIPOLYGON':
        geom: MultiPolygon = geom
        for sub_geom in geom.geoms:
            sub_geom: Polygon = sub_geom
            one_list = []
            for coord in sub_geom.exterior.coords:
                one_list.append(','.join([str(round(coord[0], 6)), str(round(coord[1], 6))]))
            result_list.append(';'.join(one_list))
    elif geom.geom_type.upper() == 'POINT':
        result_list.append(','.join([
            str(round(geom.coords[0][0], 6)),
            str(round(geom.coords[0][1], 6)),
        ]))
    else:
        one_list = []
        for coord in geom.coords:
            one_list.append(','.join([str(round(coord[0], 6)), str(round(coord[1], 6))]))
        result_list.append(';'.join(one_list))
        pass

    return '#'.join(result_list)
