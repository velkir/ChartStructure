from Data_preprocess import download_ccxt
from FindTrends import getTrends
import json
from Logging import setup_logging

logger = setup_logging()

df = download_ccxt(Market="BTC/USDT", Since='2022-01-01T00:00:00Z', To='2023-05-01T00:00:00Z',Timeframe="1M")
rootTrends = getTrends(dataframe=df, minthreshold=0.1, logger=logger)

json_data = [trend.to_dict() for trend in rootTrends]
json_final = json.dumps(json_data)
with open('trends.json', 'w') as file:
    file.write(json_final)
