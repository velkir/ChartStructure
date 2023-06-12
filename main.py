from Data_preprocess import download_ccxt
from FindTrends import getTrends
import json
from Logging import setup_logging
import sys
import time
import cProfile
import pstats

logger = setup_logging()

#На большом объеме данных достигает лимита. По-хорошему - поставить цикл вместо рекурсии
sys.setrecursionlimit(4000)

df = download_ccxt(Market="BTC/USDT", Since='2016-05-10T00:00:00Z', To='2023-06-23T00:00:00Z',Timeframe="1M")

start_time = time.time()
# cProfile.run('rootTrends = getTrends(dataframe=df, minthreshold=0.2, logger=logger)', 'output_file.prof')
rootTrends = getTrends(dataframe=df, minthreshold=0.2, logger=logger)
end_time = time.time()
p = pstats.Stats('output_file.prof')
p.sort_stats('cumulative').print_stats(10)


execution_time = end_time - start_time

print("Execution time: ", execution_time, "seconds")

json_data = [trend.to_dict() for trend in rootTrends]
json_final = json.dumps(json_data)
with open('trends.json', 'w') as file:
    file.write(json_final)
