#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import datetime
import time
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.pyplot as plt
import json
import math

from bigdata_util.connector.base_query import IBaseQuery
from ..connector import MaxComputeConnector
from ..util import get_logger

matplotlib.rc('font', family='Arial Unicode MS')
logger = get_logger(__file__)


class PlotLine:
    __cnt = 1

    def __init__(self, db_ins: IBaseQuery):
        self.o = db_ins
        pass

    def new_figure(self):
        self.__cnt += 1
        return plt.figure(self.__cnt)

    def plot_line(self, sql, title='my title', labels=[], groups=[], rotation=30, show_legend=True):
        fig = self.new_figure()
        logger.info('running sql: ' + sql)
        data_list = self.o.run_sql_return_plain_json(sql)
        if len(data_list) == 0:
            logger.error('No data found with sql')
            return
        column_names = data_list[0].keys()

        if len(labels) == 0:
            if 'label' in column_names:
                labels.append('label')
            i = 1
            while ('label' + str(i)) in column_names:
                labels.append('label' + str(i))
                i += 1

        data_list.sort(key=lambda x: x['x'])
        x_meta = {}
        to_plot_data = {}

        for rd in data_list:
            label_key = 'default' if len(labels) == 0 else ','.join(
                list(map(
                    lambda l: rd[l],
                    labels
                ))
            )
            if label_key not in to_plot_data:
                to_plot_data[label_key] = {
                    'x': [],
                    'y': [],
                    'label': label_key
                }
            to_plot_data[label_key]['x'].append(rd['x'])
            to_plot_data[label_key]['y'].append(rd['y'])
            x_meta[rd['x']] = 0

        xs = list(x_meta.keys())
        xs.sort()
        for i, x in enumerate(xs):
            x_meta[x] = i + 1

        for key in to_plot_data:
            meta = to_plot_data[key]
            for i, x in enumerate(meta['x']):
                meta['x'][i] = x_meta[x]
            # plt.plot(meta['x'], meta['y'], zorder=1, label=meta['label'])
            plt.plot(range(len(meta['x'])), meta['y'], zorder=1, label=meta['label'])
            # if meta['label'] == u'均值':
            #   plt.plot(meta['x'], meta['y'], 'b.-', zorder=2, label=meta['label'])
            # else:
            #   plt.plot(meta['x'], meta['y'], zorder=1, label=meta['label'])

        if len(labels) > 0 and show_legend:
            plt.legend(loc='upper right')

        x_ticks_id = []
        x_ticks_label = []
        # if False:
        if len(xs) > 20:
            step = math.floor(len(xs) / 10)
            valid_i = list(filter(
                lambda i: True if i % step == 0 else False,
                range(len(xs))
            ))
            x_ticks_label = [xs[i] for i in valid_i]
        else:
            x_ticks_label = xs
        x_ticks_id = [x_meta[x] for x in x_ticks_label]

        plt.xticks(x_ticks_id, x_ticks_label, rotation=rotation)
        plt.title(title)
        fig.show()
        pass

    @staticmethod
    def show():
        plt.show()
