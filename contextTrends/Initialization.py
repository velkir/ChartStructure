import configparser

def initialize():
    config = configparser.ConfigParser()
    config.read('config.ini')
    minDelta = config.getfloat('Settings', 'min_trend_delta')
    Market = config.get('Settings', 'Market')
    Since = config.get('Settings', 'Since')
    To = config.get('Settings', 'To')
    Timeframe = config.get('Settings', 'Timeframe')

    return minDelta, Market, Since, To, Timeframe