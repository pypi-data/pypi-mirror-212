#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='py-bigdata-util',
    version='0.1.0',
    description=(
      'Bigdata Utility Code.'
    ),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Albin',
    author_email='binwei.zeng3@gmail.com',
    maintainer='albin3',
    maintainer_email='binwei.zeng3@gmail.com',
    license='',
    packages=[
        'bigdata_util',
        'bigdata_util.util',
        'bigdata_util.plot',
        'bigdata_util.connector',
    ],
    platforms=["all"],
    url='https://gitee.com/albin3/py-bigdata-util',
    include_package_data=True,
    install_requires=[
        'fire',
        'configobj',
        'pydash',
        'shapely',
        'pyhocon',
        'pandas',
        'asyncio',
        'pysocks',
        'numpy',
        # 'scikit-learn',
        # 'sklearn2pmml',
        # 'pyodps==0.9.1',
        'pyodps==0.11.2.1',
        # 'pydatahub==2.17.0',
        'psycopg2-binary',
        # 'geopandas==0.9.0',
        # 'pyproj==3.2.1'
    ],
    scripts=[
    ],
    classifiers=[
    ],
)
