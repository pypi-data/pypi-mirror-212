#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from . import get_logger
from pyhocon import ConfigFactory, HOCONConverter, ConfigTree
import os
import pydash

logger = get_logger(__file__)


class BaseConfig(ConfigTree):
    def __init__(self, *args, **kwargs):
        super(BaseConfig, self).__init__(*args, **kwargs)

    @staticmethod
    def load_from_file(*args):
        """
        从文件中load配置
        :param config_file_path:
        :return:
        """
        result_config = ConfigTree()
        for file_path in args:
            ConfigTree.merge_configs(result_config, BaseConfig(ConfigFactory.parse_file(file_path, required=False)), copy_trees=False)
        return BaseConfig(result_config)
