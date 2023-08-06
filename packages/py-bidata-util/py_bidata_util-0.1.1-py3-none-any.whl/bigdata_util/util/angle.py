#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from .logger import get_logger
from .shapely_helper import transform_to_epgs3857
import math
from shapely.geometry import Point
from typing import List

logger = get_logger(__name__)


def normalize_point(point):
    if isinstance(point, Point):
        return point

    if isinstance(point, str):
        p = list(map(
            lambda z: float(z),
            point.split(',')
        ))
        return Point(p[0], p[1])

    if isinstance(point, List):
        return Point(point[0], point[1])

    return Point(point[0], point[1])


def angle_with_north_of_epsg3857(point1, point2, is_radian=True):
    """
    计算点1和点2的角度，判断点1和点2是否是epsg3857坐标系下的坐标，如果不是的话，自动转换为该坐标系
    :param point1:
    :param point2:
    :param is_radian:
    :return:
    """
    n_p1 = normalize_point(point1)
    n_p2 = normalize_point(point2)

    if -180 <= n_p1.x <= 180 and -90 <= n_p1.y <=90:
        n_p1 = transform_to_epgs3857(n_p1)
    if -180 <= n_p2.x <= 180 and -90 <= n_p2.y <=90:
        n_p2 = transform_to_epgs3857(n_p2)

    return angle_with_north(n_p1, n_p2, is_radian=is_radian)


def angle_with_north(point1, point2, is_radian=True):
    """
    计算point1, point2的两点连线，与正北方向的顺时针角度。
    """
    point1 = normalize_point(point1)
    point2 = normalize_point(point2)

    diff_x = point2.x - point1.x
    diff_y = point2.y - point1.y
    length = math.sqrt(diff_x ** 2 + diff_y ** 2)
    angle = math.acos(diff_y / length)

    if diff_x < 0:
        angle = -1 * angle

    if angle < 0:
        angle += 2 * math.pi

    if is_radian:
        return angle
    else:
        return round(angle * 180 / math.pi, 6)


def adjust_f_angle_in_inter_ftrid(lnglat_seq: str):
    """
    由于inter_ftrid表的字段值与描述不符，自己计算角度
    :param angle:
    :return:
    """
    lnglat_seq_list = lnglat_seq.split(';')
    second_point = lnglat_seq_list[-1]
    idx = len(lnglat_seq_list) - 1
    while idx >= 0 and lnglat_seq_list[idx] == second_point:
        idx -= 1
    first_point = lnglat_seq_list[idx]
    if first_point == second_point:
        return 0.0

    first_point = first_point.split(',')
    second_point = second_point.split(',')
    first_point = list(map(lambda x: float(x), first_point))
    second_point = list(map(lambda x: float(x), second_point))
    return angle_with_north_of_epsg3857(first_point, second_point) * 180 / math.pi;


def min_diff_angle(angle1, angle2):
    """
    计算两个角度的夹角(小于180度)
    :param angle1: 0-360
    :param angle2: 0-360
    :return:
    """
    diff_angle1 = (angle1 - angle2 + 360) % 360
    diff_angle2 = (angle2 - angle1 + 360) % 360

    return diff_angle1 if diff_angle1 < diff_angle2 else diff_angle2


def reverse_angle(angle, is_radian=False):
    if is_radian:
        return (angle + math.pi) % (2 * math.pi)
    else:
        return (angle + 180) % 360
    pass


if __name__ == "__main__":
    logger.info(angle_with_north([0, 0], [0, 1]) / math.pi * 180)
    logger.info(angle_with_north([0, 0], [1, 1]) / math.pi * 180)
    logger.info(angle_with_north([0, 0], [1, 0]) / math.pi * 180)
    logger.info(angle_with_north([0, 0], [1, -1]) / math.pi * 180)
    logger.info(angle_with_north([0, 0], [0, -1]) / math.pi * 180)
    logger.info(angle_with_north([0, 0], [-1, -1]) / math.pi * 180)
    logger.info(angle_with_north([0, 0], [-1, 0]) / math.pi * 180)
    logger.info(angle_with_north([0, 0], [-1, 1]) / math.pi * 180)
    pass
