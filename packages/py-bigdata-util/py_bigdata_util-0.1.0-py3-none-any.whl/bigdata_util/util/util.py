#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import asyncio
import datetime
import os


def get_compare_by_key_func(key: str):
    def compare_func(a, b='b_string'):
        return a[key] - b[key]

    return compare_func


def get_reduce_list_to_map_func(key: str):
    def reduce_list_to_map(x, y):
        x[y[key]] = y
        return x

    return reduce_list_to_map


def shapely_ops_substring(geom, start_dist, end_dist, normalized=False):
    """Return a line segment between specified distances along a linear geometry.
    Negative distance values are taken as measured in the reverse
    direction from the end of the geometry. Out-of-range index
    values are handled by clamping them to the valid range of values.
    If the start distances equals the end distance, a point is being returned.
    If the normalized arg is True, the distance will be interpreted as a
    fraction of the geometry's length.
    """
    from shapely.geometry import LineString, Point

    assert (isinstance(geom, LineString))

    # Filter out cases in which to return a point
    if start_dist == end_dist:
        return geom.interpolate(start_dist, normalized)
    elif not normalized and start_dist >= geom.length and end_dist >= geom.length:
        return geom.interpolate(geom.length, normalized)
    elif not normalized and -start_dist >= geom.length and -end_dist >= geom.length:
        return geom.interpolate(0, normalized)
    elif normalized and start_dist >= 1 and end_dist >= 1:
        return geom.interpolate(1, normalized)
    elif normalized and -start_dist >= 1 and -end_dist >= 1:
        return geom.interpolate(0, normalized)

    start_point = geom.interpolate(start_dist, normalized)
    end_point = geom.interpolate(end_dist, normalized)

    min_dist = min(start_dist, end_dist)
    max_dist = max(start_dist, end_dist)
    if normalized:
        min_dist *= geom.length
        max_dist *= geom.length

    vertex_list = [(start_point.x, start_point.y)]
    coords = list(geom.coords)
    for p in coords:
        pd = geom.project(Point(p))
        if pd <= min_dist:
            pass
        elif min_dist < pd < max_dist:
            vertex_list.append(p)
        else:
            break
    vertex_list.append((end_point.x, end_point.y))

    # reverse direction of section
    if start_dist > end_dist:
        vertex_list = reversed(vertex_list)

    return LineString(vertex_list)


def get_absolute_path(base_path, relative_path):
    return os.path.abspath(os.path.join(
        os.path.split(os.path.realpath(base_path))[0], relative_path
    ))


def partition_to_where(partition: str):
    partition_col_list = partition.replace('/', ',').split(',')

    where_item_list = []
    for partition_info in partition_col_list:
        kv = partition_info.split('=')
        if len(kv) < 2:
            where_item_list.append('1=1')
            continue
        if not (kv[1][0] == "'" and kv[1][-1] == "'") and not (kv[1][0] == '"' and kv[1][-1] == '"'):
            where_item_list.append(kv[0] + '=' + "'" + kv[1] + "'")
        else:
            where_item_list.append(kv[0] + '=' + kv[1])
        pass

    if len(where_item_list) == 0:
        where_item_list.append('1=1')

    return ' and '.join(where_item_list)


def get_week_last_day(yyyymmdd: str) -> str:
    """
    输入日期，返回这个日期最近的的下一个星期天，可以是它自己
    :param yyyymmdd:
    :return:
    """
    dt = datetime.datetime.strptime(yyyymmdd, '%Y%m%d')
    one_day = datetime.timedelta(days=1)

    # weekday 从周一到周日分别是 0~6
    while dt.weekday() != 6:
        dt += one_day

    return dt.strftime('%Y%m%d')


def get_n_days_ago(yyyymmdd: str, n: int) -> str:
    """
    返回输入日期，n天前的日期
    :param yyyymmdd:
    :param n:
    :return:
    """
    dt = datetime.datetime.strptime(yyyymmdd, '%Y%m%d')
    date_diff = datetime.timedelta(days=-1 * n)
    dt = dt + date_diff

    return dt.strftime('%Y%m%d')


def get_first_day_of_month(yyyymmdd: str) -> str:
    """
    返回本月的第一天
    :param yyyymmdd:
    :return:
    """
    dt = datetime.datetime.strptime(yyyymmdd, '%Y%m%d')
    return dt.strftime('%Y%m01')


def check_real_vhc_no_valid() -> str:
    return '''
        REGEXP_EXTRACT(vhc_no,
           '^(([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z](([0-9]{5}[DF])|([DF]([A-HJ-NP-Z0-9])[0-9]{4})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳使领]))$',
            1) <> '' = true
    '''


def check_mapped_vhc_no_valid() -> str:
    return '''
        vhc_no is not null and vhc_no != 'UNKNOWN' and vhc_no != 'unknown'
    '''


def get_last_sunday(dt: str) -> str:
    if get_week_last_day(dt) == dt:
        return dt
    else:
        return get_n_days_ago(get_week_last_day(dt), 7)
    pass

def get_datetime_range(*kw, **kwargs):
    return get_date_range(*kw, **kwargs)

def get_date_range(
        start_dt, end_dt, date_format='%Y%m%d', delta_time=datetime.timedelta(days=1),
        strict=True, contains_end=True
    ):
    datetime_list = []
    begin_date = datetime.datetime.strptime(start_dt, date_format)
    end_date = datetime.datetime.strptime(end_dt, date_format)

    diff_days = (end_date - begin_date).days
    if diff_days < 0:
        raise Exception('开始时间大于结束时间')
    if strict and diff_days > 1000:
        raise Exception('strict 模式下，时间范围不能超过1000天，可以设置 strict=False 突破限制！')
    one_step = delta_time

    while begin_date < end_date:
        date_str = begin_date.strftime(date_format)
        datetime_list.append(date_str)
        begin_date += one_step

    if contains_end and begin_date == end_date:
        date_str = begin_date.strftime(date_format)
        datetime_list.append(date_str)

    return datetime_list

def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop


if __name__ == '__main__':
    print(get_week_last_day('20190505'))
