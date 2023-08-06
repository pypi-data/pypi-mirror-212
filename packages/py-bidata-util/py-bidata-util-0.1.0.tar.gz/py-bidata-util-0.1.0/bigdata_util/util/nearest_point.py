#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import List
from .logger import get_logger
from .shapely_helper import transform_to_euclidean_coordinate, transform_to_epsg4326
from shapely.geometry import LineString, Point
from shapely import ops as shapely_ops
import numpy as np
import math

logger = get_logger(__name__)


def is_same_point(p1, p2):
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return True
    else:
        return False


def cal_distance(point1=(0, 0), point2=(1, 1)):
    d = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    return d


def cal_euclid_distance(point1=(0, 0), point2=(1, 1)):
    line: LineString = LineString([point1, point2])
    euclid_line: LineString = transform_to_euclidean_coordinate(line)
    return euclid_line.length


def nearest_2_different_point_on_lnglat_seq(lnglat_seq='1,1;2,2;3,3', point=(1, 1)):
    """
    找一个点到lnglat_seq序列中的最近2个点，按照在lnglat_seq中的顺序返回
    """
    lnglat_list = list(map(
        lambda x: (float(x.split(',')[0]), float(x.split(',')[1])),
        lnglat_seq.split(';')
    ))

    distance_list = [{
        'point': x,
        'distance': cal_distance(point, x),
        'idx': idx
    } for idx, x in enumerate(lnglat_list)]

    distance_list.sort(key=lambda x: x['distance'])

    if len(distance_list) == 0:
        return []
    if len(distance_list) == 1:
        return [x['point'] for x in distance_list]

    while len(distance_list) > 1:
        if is_same_point(distance_list[0]['point'], distance_list[1]['point']):
            distance_list = distance_list[1:]
        else:
            break

    distance_list = distance_list[:2]
    if distance_list[0]['idx'] > distance_list[1]['idx']:
        distance_list.reverse()
    return [x['point'] for x in distance_list]


def find_nearest_point_on_seq(lnglat_seq='1,1;2,2;3,3', point=(1, 1)):
    """
    找到lnglat_seq序列中到目标点最近的点
    :param lnglat_seq:
    :param point:
    :return:
    """
    lnglat_list = list(map(
        lambda x: (float(x.split(',')[0]), float(x.split(',')[1])),
        lnglat_seq.split(';')
    ))

    distance_list = [{
        'point': x,
        'distance': cal_distance(point, x),
        'idx': idx
    } for idx, x in enumerate(lnglat_list)]

    # distance_list.sort(key=lambda x: x['distance'])

    min_distance = -1.0
    min_distance_meta_before_point = None  # 需要找到到达这个点之前的最后一个序列
    for idx, meta in enumerate(distance_list):
        # if min_distance < 0 or meta['distance'] <= min_distance:
        if min_distance < 0 or meta['distance'] < min_distance:
            min_distance = meta['distance']
            min_distance_meta_before_point = meta
        else:
            continue

    return [min_distance_meta_before_point['point']]

    # if len(distance_list) == 0:
    #     return []
    # if len(distance_list) == 1:
    #     return [x['point'] for x in distance_list]

    # distance_list = distance_list[:1]
    # return [x['point'] for x in distance_list]


def find_nearest_point_on_line(lnglat_seq: str, specified_point: List[float]):
    """
    在轨迹序列所在的线段上，找到离指定点最近的点(点不一定在轨迹序列中)
    :param lnglat_seq:
    :param specified_point:
    :return:
    """
    lnglat_seq_list: List[str] = lnglat_seq.split(';')
    if len(lnglat_seq_list) < 2:
        raise Exception('parameter lnglat_seq is illegal: ' + lnglat_seq_list + '.')
    if len(specified_point) != 2:
        raise Exception('parameter cursor is illegal: ' + specified_point + '.')

    line_string: LineString = LineString(list(map(lambda p: list(map(lambda x: float(x), p.split(','))),
                                                  lnglat_seq.split(';'))))
    point: Point = Point(specified_point)
    line_string: LineString = transform_to_euclidean_coordinate(line_string)
    point: Point = transform_to_euclidean_coordinate(point)

    nearest_points = shapely_ops.nearest_points(line_string, point)
    result_point: Point = transform_to_epsg4326(nearest_points[0])

    return [result_point.x, result_point.y]


def find_nearest_point_on_sequence_before_and_after_specified_point(
        lnglat_seq: str, specified_point: List[float], is_start_or_end_cross_id: bool = False
) -> List[List[float]]:
    """
    返回经纬度序列中，在给定点之后离给定点最近的前后两个点(可与给定点相同)
    :rtype: object
    :param lnglat_seq: 经纬度序列，";"分割点，","分割经度和纬度
    :param specified_point: 给定点
    :param is_start_or_end_cross_id: 起止点cross_id
    :return:  经纬度中的点
    """
    lnglat_seq_list: List[str] = lnglat_seq.split(';')
    if len(lnglat_seq_list) < 2:
        raise Exception('parameter lnglat_seq is illegal: ' + lnglat_seq_list + '.')
    if len(specified_point) != 2:
        raise Exception('parameter cursor is illegal: ' + specified_point + '.')

    # 0. 快速返回
    lnglat_point_seq: List[List[float]] = list(map(
        lambda p: list(map(lambda x: float(x), p.split(','))),
        lnglat_seq.split(';')
    ))
    size = len(lnglat_point_seq)
    nearest_point_on_seq = find_nearest_point_on_seq(lnglat_seq, specified_point)

    if is_start_or_end_cross_id:
        return [nearest_point_on_seq[0], nearest_point_on_seq[0]]

    if size > 2 and not np.any(np.subtract(lnglat_point_seq[size - 1], nearest_point_on_seq[0])):
        return [lnglat_point_seq[size - 1], lnglat_point_seq[size - 1]]
    if size > 2 and not np.any(np.subtract(lnglat_point_seq[0], nearest_point_on_seq[0])):
        return [lnglat_point_seq[0], lnglat_point_seq[0]]

    # 1. 找到在该线段上(可以不再sequence中)离目标点最近的点
    nearest_point_on_line = find_nearest_point_on_line(lnglat_seq, specified_point)
    nearest_point_on_line = list(map(
        lambda x: round(x, 6),
        nearest_point_on_line
    ))

    # 2. 使用向量相乘，找到出现反转的点
    for idx, lnglat_point in enumerate(lnglat_point_seq):
        if idx == len(lnglat_point_seq) - 1:
            continue
        next_lnglat_point = lnglat_point_seq[idx + 1]
        vec1: np.ndarray = np.subtract(lnglat_point, nearest_point_on_line)
        vec2: np.ndarray = np.subtract(next_lnglat_point, nearest_point_on_line)

        # if abs(vec1[0]) < 1e-5 and abs(vec1[1]) < 1e-5:
        #     return [lnglat_point, lnglat_point]
        # if abs(vec2[0]) < 1e-5 and abs(vec2[1]) < 1e-5:
        #     return [next_lnglat_point, next_lnglat_point]

        # 返回在指定点之前和之后的点
        if np.sum(np.multiply(vec1, vec2)) < 0:
            return [lnglat_point, next_lnglat_point]

    return [nearest_point_on_seq[0], nearest_point_on_seq[0]]
