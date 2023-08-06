# coding=UTF-8
import sys
from pathlib import Path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    


install_requires = [
    'pandas == 1.2.5',
    'numpy == 1.22.3',
    'exchange-calendars == 3.3.0',
    'requests >= 2.7.0',
    'inflection >= 0.3.1',
    'python-dateutil',
    'six',
    'more-itertools',
    'tejapi',
    'matplotlib',
    'babel',
    'Jinja2',
    'ipython',
    'matplotlib-inline',
    'pyzmq',
    'tornado',
    'psutil',
    'pyyaml',
    'snowballstemmer',
    'sphinxcontrib-applehelp',
    'sphinxcontrib-devhelp',
    'sphinxcontrib-htmlhelp',
    'sphinxcontrib-jsmath',
    'sphinxcontrib-qthelp',
    'sphinxcontrib-serializinghtml',
    'tinycss2',
    'pywin32-ctypes',
    'nest-asyncio',
    'traitlets',
    'python-slugify',
    'click',
    'Pygments',
    'pyfolio-reloaded==0.9.4',
    'alphalens-reloaded==0.4.2',
    'empyrical-reloaded==0.5.8',
]

installs_for_two = [
    'pyOpenSSL',
    'ndg-httpsclient',
    'pyasn1'
]

if sys.version_info[0] < 3:
    install_requires += installs_for_two

packages = [
    'zipline-tej',
    'zipline-tej.assets',
    'zipline-tej.data',
    'zipline-tej.examples',
    'zipline-tej.finance',
    'zipline-tej.gens',
    'zipline-tej.lib',
    'zipline-tej.pipeline',
    'zipline-tej.resources',
    'zipline-tej.testing',
    'zipline-tej.utils',
    'zipline-tej.data.bundles',
    'zipline-tej.data.fx',
    'zipline-tej.finance.blotter',
    'zipline-tej.finance.metrics',
    'zipline-tej.pipeline.classifiers',
    'zipline-tej.pipeline.data',
    'zipline-tej.pipeline.factors',
    'zipline-tej.pipeline.filters',
    'zipline-tej.pipeline.hooks',
    'zipline-tej.pipeline.loaders',
    'zipline-tej.resources.market_data',
    'zipline-tej.resources.security_lists',
    'zipline-tej.resources.security_lists.leveraged_etf_list',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20120913',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20120919',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20121012',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20130605',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20130916',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20131002',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20131009',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20131121',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20131227',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20140410',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20140923',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20141119',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20141226',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20150123',
    'zipline-tej.resources.security_lists.leveraged_etf_list.20020103.20160826',
]


this_directionary = Path(__file__).parent
long_description = (this_directionary/"README.md").read_text(encoding='utf-8')
setup(
    name='zipline-tej',
    description='Package for stock backtesting modified by TEJ.',
    keywords=['tej', 'zipline', 'data', 'financial', 'economic','stock','backtest','TEJ',],
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.10',
    author='tej',
    author_email='tej@tej.com.tw',
    maintainer='tej api Development Team',
    maintainer_email='tej@tej.com',
    url='https://api.tej.com.tw',
    license='MIT',
    install_requires=install_requires,
    tests_require=[
        'unittest2',
        'flake8',
        'nose',
        'httpretty',
        'mock',
        'factory_boy',
        'jsondate'
    ],
    test_suite="nose.collector",
    packages=packages,
    package_data = {'': ['add','delete','*.csv']},
    include_package_data=True,
)