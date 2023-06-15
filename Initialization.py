from Data_preprocess import download_ccxt
from FindTrends import getTrends
import json
from Logging import setup_logging
import sys
import time
import cProfile
import pstats
import configparser

def initialize():
    logger = setup_logging()
    config = configparser.ConfigParser()
    config.read('config.ini')
    correction_ratio = config.getfloat('Settings', 'correction_ratio')
    min_trend_delta = config.getfloat('Settings', 'min_trend_delta')
    Market = config.get('Settings', 'Market')
    Since = config.get('Settings', 'Since')
    To = config.get('Settings', 'To')
    Timeframe = config.get('Settings', 'Timeframe')
    # На большом объеме данных достигает лимита. По-хорошему - поставить цикл вместо рекурсии
    sys.setrecursionlimit(4000)
    return logger, correction_ratio, min_trend_delta, Market, Since, To, Timeframe