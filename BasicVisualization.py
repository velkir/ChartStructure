import pandas as pd
import plotly.graph_objects as go
from Data_preprocess import download_ccxt

df = download_ccxt(Market="BTC/USDT", Since='2020-12-11T00:00:00Z', To='2023-08-01T00:00:00Z',Timeframe="1d")

# Чтение данных из txt файла и преобразование их в DataFrame
trends = pd.read_csv('trends.txt', header=None)
trends.columns = ['direction', 'point0', 'point1', 'parent', 'status', 'delta', 'timestampstart', 'timestampend']
trends['timestampstart'] = pd.to_datetime(trends['timestampstart'])
trends['timestampend'] = pd.to_datetime(trends['timestampend'])

# Создание графика OHLC
fig = go.Figure(data=go.Ohlc(x=df['timestamp'],
                    open=df['OPEN'],
                    high=df['HIGH'],
                    low=df['LOW'],
                    close=df['CLOSE']))

# Добавление данных о трендах на график
for index, row in trends.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['timestampstart'], row['timestampend']],
        y=[row['point0'], row['point1']],
        mode='lines+markers',
        name=f'Trend {index+1}'
    ))

# Обновление параметров графика
fig.update_layout(
    title='BTCUSDT Price and Trends Over Time',
    xaxis_title='Timestamp',
    yaxis_title='Price / Trend Points',
    autosize=False,
    width=1000,
    height=600,
)

# Отображение графика
fig.show()


# import matplotlib.pyplot as plt
# from Data_preprocess import download_ccxt
# import plotly.graph_objects as go
# df = download_ccxt(Market="BTC/USDT", Since='2017-12-11T00:00:00Z', To='2023-08-01T00:00:00Z',Timeframe="1w")
#
# fig = go.Figure(data=go.Ohlc(x=df['timestamp'],
#                     open=df['OPEN'],
#                     high=df['HIGH'],
#                     low=df['LOW'],
#                     close=df['CLOSE']))
#
# fig.update_layout(
#     title='BTCUSDT Price Over Time',
#     xaxis_title='Timestamp',
#     yaxis_title='Price (USDT)',
#     autosize=False,
#     width=1000,
#     height=600,
# )
#
# fig.show()