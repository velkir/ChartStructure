import ccxt
import datetime
import pandas as pd
import logging

def download_ccxt(Market, Since, To, Timeframe, Exchange=ccxt.binance()):
    logger = logging.getLogger('download_ccxt')
    logger.propagate = False
    # Initialize Binance API
    exchange = Exchange
    # exchange = ccxt.binance()

    # Define the market and timeframe
    market = Market
    # market = 'DOGE/USDT'
    timeframe = Timeframe  # 4 hour timeframe
    # timeframe = '4h'

    # Define the date range
    since = exchange.parse8601(Since)
    to = exchange.parse8601(To)
    # since = exchange.parse8601('2017-01-01T00:00:00Z')  # 01-01-2015
    # to = exchange.parse8601('2023-08-01T00:00:00Z')  # 01-06-2023

    # Empty list to hold data
    data = []

    # Fetch OHLCV data in batches
    while since < to:
        try:
            print(f'Fetching OHLCV data since {exchange.iso8601(since)}')
            ohlcv = exchange.fetch_ohlcv(market, timeframe, since)
            if len(ohlcv) == 0:
                break
            else:
                data.extend(ohlcv)
                since = ohlcv[-1][0] + 1  # Update 'since' to the timestamp of the last data point + 1 millisecond
        except Exception as e:
            print(f'Error occurred: {e}')
            break

    print(f'Fetched {len(data)} data points')

    # Process data
    df = pd.DataFrame(data, columns=['timestamp', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL'])

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    filename = str(f"{market.replace('/', '')}_{str(datetime.datetime.strptime(Since, '%Y-%m-%dT%H:%M:%SZ').date()).replace('-', '')}_{str(datetime.datetime.strptime(To, '%Y-%m-%dT%H:%M:%SZ').date()).replace('-', '')}_{timeframe}")
    df.to_csv("csv/" + filename +".csv", index=False)
    # df.to_csv("ohlc.csv")
    # Split timestamp into date and time columns
    # df['DATE'] = df['timestamp'].dt.strftime('%Y%m%d')
    # df['TIME'] = df['timestamp'].dt.strftime('%H%M%S')

    return df, filename

def convert_to_heiken_ashi(df):
    df = df.copy()  # Создаем копию, чтобы не изменять исходный DataFrame

    # Создаем новые колонки для данных Heiken Ashi
    df['HA_Close'] = (df['OPEN'] + df['HIGH'] + df['LOW'] + df['CLOSE']) / 4
    df['HA_Open'] = 0.0
    df['HA_High'] = 0.0
    df['HA_Low'] = 0.0

    # Проходим по всем строкам в DataFrame и заполняем колонки Heiken Ashi
    for i in range(len(df)):
        if i == 0:
            df.at[i, 'HA_Open'] = (df.at[i, 'OPEN'] + df.at[i, 'CLOSE']) / 2
        else:
            df.at[i, 'HA_Open'] = (df.at[i - 1, 'HA_Open'] + df.at[i - 1, 'HA_Close']) / 2
        df.at[i, 'HA_High'] = max(df.at[i, 'HIGH'], df.at[i, 'HA_Open'], df.at[i, 'HA_Close'])
        df.at[i, 'HA_Low'] = min(df.at[i, 'LOW'], df.at[i, 'HA_Open'], df.at[i, 'HA_Close'])

    # Удаляем оригинальные колонки
    df.drop(columns=['OPEN', 'HIGH', 'LOW', 'CLOSE'], inplace=True)

    # Переименовываем новые столбцы
    df.rename(columns={'HA_Open': 'OPEN', 'HA_High': 'HIGH', 'HA_Low': 'LOW', 'HA_Close': 'CLOSE'}, inplace=True)
    df.to_csv("heiken.csv")
    return df[['timestamp', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL']]

def get_trading_view_data():
    df = pd.read_csv("BITSTAMP_ETHUSD, 1W.csv")
    df = df.drop(columns=['Volume MA', 'RSI', 'RSI-based MA', 'Upper Bollinger Band', 'Lower Bollinger Band'])
    df = df.rename(columns={
        'time': 'timestamp',
        'open': 'OPEN',
        'high': 'HIGH',
        'low': 'LOW',
        'close': 'CLOSE',
        'Volume': 'VOL'
    })
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.to_csv("ETHUSD.csv", index=False)
    return df