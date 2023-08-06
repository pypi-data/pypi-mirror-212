#!/usr/bin/env python3
# -*- coding=utf-8 -*-


from .csv import load_csv
from .csv import save_csv
from .csv import empty_csv

from .logger import get_logger

from .str_format import lnglat_seq_2_wkt, safe_get_and_not_none, get_lnglat_seq

# from .angle import angle_with_north_of_epsg3857
# from .angle import adjust_f_angle_in_inter_ftrid
# from .angle import min_diff_angle
# from .angle import reverse_angle

# from .nearest_point import nearest_2_different_point_on_lnglat_seq
# from .nearest_point import find_nearest_point_on_seq
# from .nearest_point import find_nearest_point_on_line
# from .nearest_point import cal_euclid_distance
# from .nearest_point import cal_distance
# from .nearest_point import find_nearest_point_on_sequence_before_and_after_specified_point

# from .shapely_helper import transform_to_euclidean_coordinate, transform_to_epsg4326, transform_to_epgs3857, merge_pools, transform_to_aea

from .base_config import BaseConfig

from .singleton import Singleton

from .util import get_reduce_list_to_map_func
from .util import get_compare_by_key_func
from .util import shapely_ops_substring
from .util import get_absolute_path
from .util import partition_to_where
from .util import get_week_last_day
from .util import get_n_days_ago
from .util import get_first_day_of_month
from .util import get_last_sunday
from .util import get_date_range
from .util import get_event_loop

from .sql_format import replace_placeholder_in_file

from .network import set_proxy_global, reset_proxy_global
