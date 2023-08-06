#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import List
import hashlib

try:
    import pyproj
    if pyproj.__version__ < '2.0.0':
        from functools import partial
        transformer_4326_3857 = partial(
            pyproj.transform,
            pyproj.Proj(init='EPSG:4326'),
            pyproj.Proj(init='EPSG:3857'),
        )
        transformer_3857_4326 = partial(
            pyproj.transform,
            pyproj.Proj(init='EPSG:3857'),
            pyproj.Proj(init='EPSG:4326'),
        )
        pass
    else:
        from pyproj.transformer import Transformer
        transformer_4326_3857 = Transformer.from_crs(4326, 3857, always_xy=True).transform
        transformer_3857_4326 = Transformer.from_crs(3857, 4326, always_xy=True).transform
except ImportError:
    pass

from shapely.geometry import LineString, Point

def get_transformer_4326_3857():
    return transformer_4326_3857


def get_transformer_3857_4326():
    return transformer_3857_4326


def get_aea_proj():
    if pyproj.__version__ < '2.0.0':
        aea_proj = pyproj.Proj(
            proj='aea',
            lat1=10.0,
            lat2=50.0,
        )
    else:
        aea_proj = pyproj.Proj(
            proj='aea',
            # 下面的纬度参数写死，在中国区域(北纬)，不影响长度和面积的计算，同时可以保证经过转换的geometry之间的可比性(比如distance计算)
            lat_1=10.0,
            lat_2=50.0,
            lat1=10.0,
            lat2=50.0,
            always_xy=True,
        )
    return aea_proj


def get_transformer_4326_aea():
    import pyproj

    if pyproj.__version__ < '2.0.0':
        from functools import partial
        transformer_4326_aea = partial(
            pyproj.transform,
            pyproj.Proj(init='EPSG:4326'),
            get_aea_proj(),
        )
    else:
        from pyproj.transformer import Transformer
        transformer_4326_aea = Transformer.from_proj(
            pyproj.Proj('EPSG:4326'),
            get_aea_proj(),
            always_xy=True
        ).transform
    return transformer_4326_aea


def get_transformer_aea_4326():
    import pyproj

    if pyproj.__version__ < '2.0.0':
        from functools import partial
        transformer_aea_4326 = partial(
            pyproj.transform,
            get_aea_proj(),
            pyproj.Proj(init='EPSG:4326'),
        )
    else:
        from pyproj.transformer import Transformer
        transformer_aea_4326 = Transformer.from_proj(
            get_aea_proj(),
            pyproj.Proj('EPSG:4326'),
            always_xy=True
        ).transform
    return transformer_aea_4326


def transform_to_epgs3857(geom):
    import shapely.ops as ops
    return ops.transform(
        get_transformer_4326_3857(),
        geom
    )


def transform_from_aea_to_4326(geom):
    import shapely.ops as ops
    result = ops.transform(
        get_transformer_aea_4326(),
        geom
    )

    return result


def transform_to_aea_coordinate(geom):
    import shapely.ops as ops
    result = ops.transform(
        get_transformer_4326_aea(),
        geom
    )

    # TODO: 需要把 target_proj 的信息保存在geom上，以便逆向转换
    return result


def transform_to_aea(geom):
    return transform_to_aea_coordinate(geom)


def transform_to_euclidean_coordinate(geom):
    import shapely.ops as ops
    return ops.transform(
        get_transformer_4326_3857(),
        geom
    )


def transform_to_epsg4326(geom):
    import shapely.ops as ops
    return ops.transform(
      get_transformer_3857_4326(),
      geom
    )


def merge_pools(pool_list: List[dict]) -> dict:
    """
    输入pool_list返回合并后的pool
    :param pool_list: {'pool_id': 'hashed_pool_id', 'geom': epsg4326坐标系下的geomety对象}
    :return: {
      'pool_id': '合并后的id',
      'geom3857': 合并后epsg3857坐标系下的geometry对象,
      'geom': 合并后epsg4326坐标系下的geometry对象,
      'pool_id_list': [pool_id1, pool_id2, ...pool_idx]
    }
    """
    if len(pool_list) < 1:
        raise Exception('pool list for merge can\'t be empty')

    pool_info_list = []
    for pool_info in pool_list:
        meta = {
            'pool_id': pool_info['pool_id'],
            'geom': pool_info['geom'],
            'geom3857': transform_to_epgs3857(pool_info['geom'])
        }
        pool_info_list.append(meta)
        pass

    merged_pool = {
        'sub_pool_id_list': list(map(
            lambda x: x['pool_id'],
            pool_info_list
        )),
        'geom3857': pool_info_list[0]['geom3857'].buffer(0),
    }

    for pool_info in pool_info_list[1:]:
        merged_pool['geom3857'] = merged_pool['geom3857'].union(pool_info['geom3857'].buffer(0))
        pass
    merged_pool['geom'] = transform_to_epsg4326(merged_pool['geom3857'])

    hash_fac = hashlib.md5()
    hash_fac.update(','.join(merged_pool['sub_pool_id_list']).encode('utf-8'))
    merged_pool_id = hash_fac.hexdigest()
    merged_pool['pool_id'] = merged_pool_id

    return merged_pool


def get_distance_point_on_line_string(line: LineString, dist: int):
    return line.interpolate(dist)
