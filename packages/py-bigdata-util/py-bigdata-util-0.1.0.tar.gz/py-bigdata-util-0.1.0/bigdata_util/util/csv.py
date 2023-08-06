#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import pandas as pd
import json
import csv
import pydash as _
from .logger import get_logger

logger = get_logger(__name__)


def empty_csv(filename):
    if not filename.endswith('.csv'):
        filename += '.csv'
    with open(filename, 'w') as writer:
        writer.write('')
    pass


def load_csv(filename, sep='$'):
    if not filename.endswith('.csv') and not filename.endswith('.txt'):
        filename += '.csv'
        logger.warning('filename is not end with `.csv` or `.txt`, adding .csv to filename...')
    logger.info('loading csv "{filename}" ...'.format(filename=filename))
    if not os.access(filename, os.R_OK):
        logger.warn('File {} is not exist or not accessible to read.'.format(filename))
        return None
    try:
        df_json = pd.read_csv(filename, sep=sep)
        records = json.loads(df_json.to_json(orient='records'))
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        logger.warn(e)
        return None
    logger.info('loaded csv "%s", records number: %d.' % (filename, len(records)))
    return records


def save_csv(filename, data_list, sep='$', file_open_mode='w'):
    if not filename.endswith('.csv'):
        filename += '.csv'
    if file_open_mode == 'w':
        logger.info('saving csv "%s", total: %d' % (filename, len(data_list)))
    num = 0
    if len(data_list) < 1:
        return
    columns = list(data_list[0].keys())
    with open(filename, file_open_mode) as file:
        writer = csv.writer(file, delimiter=sep)
        if file_open_mode == 'w':
            writer.writerow(columns)
        for meta in data_list:
            row = [_.get(meta, key, None) for key in columns]
            row = [json.dumps(x) if type(x) in [dict, list] else x for x in row]
            writer.writerow(row)
            if file_open_mode == 'w' and num % 10000 == 0:
                logger.info('processed %d ' % num)
            num += 1
