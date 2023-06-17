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
    config = configparser.ConfigParser()
    config.read('config.ini')
    correction_ratio = config.getfloat('Settings', 'correction_ratio')
    min_trend_delta = config.getfloat('Settings', 'min_trend_delta')
    Market = config.get('Settings', 'Market')
    Since = config.get('Settings', 'Since')
    To = config.get('Settings', 'To')
    Timeframe = config.get('Settings', 'Timeframe')
    uncertain_coef = config.get('Settings', 'uncertain_coef')
    poor_coef = config.get('Settings', 'poor_coef')
    medium_coef = config.get('Settings', 'medium_coef')
    high_coef = config.get('Settings', 'high_coef')
    # На большом объеме данных достигает лимита. По-хорошему - поставить цикл вместо рекурсии
    sys.setrecursionlimit(4000)
    return correction_ratio, min_trend_delta, Market, Since, To, Timeframe, float(uncertain_coef), float(poor_coef), float(medium_coef), float(high_coef)