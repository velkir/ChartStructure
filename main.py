from Data_preprocess import download_ccxt
from FindTrends import getTrends
import Trend
df = download_ccxt(Market="BTC/USDT", Since='2020-12-11T00:00:00Z', To='2023-08-01T00:00:00Z',Timeframe="1d")

trends = getTrends(df, minthreshold=0.1)

with open("trends.txt", "w") as file:
    for trend in trends:
        line = f"{trend.direction},{trend.point0},{trend.point1},{trend.parent},{trend.status},{trend.delta}, {trend.timestampstart}, {trend.timestampend}\n"
        file.write(line)
# # df = download_ccxt(Market="BTC/USDT", Since='2017-01-01T00:00:00Z', To='2023-08-01T00:00:00Z', Timeframe="1w")
# # df = download_ccxt(Market="BTC/USDT", Since='2017-12-11T00:00:00Z', To='2023-08-01T00:00:00Z',Timeframe="1w")
# print(df.head())
# print(df.tail())
# print(df.loc[0, "timestamp"])
# visualize(df)
