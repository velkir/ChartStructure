from Data_preprocess import download_ccxt
from FindTrends import getTrends
import json
from Logging import setup_logging
import sys
import time
import cProfile
import pstats
import configparser
import Initialization
from DataSaving import save_to_json

correction_ratio, min_trend_delta, Market, Since, To, Timeframe, uncertain_coef, poor_coef, medium_coef, high_coef = Initialization.initialize()

df, filename = download_ccxt(Market=Market, Since=Since, To=To,Timeframe=Timeframe)

logger = setup_logging(filename)

start_time = time.time()
# cProfile.run('rootTrends = getTrends(dataframe=df, minthreshold=0.2, logger=logger)', 'output_file.prof')
rootTrends = getTrends(dataframe=df, correction_ratio=correction_ratio, min_trend_delta=min_trend_delta, uncertain_coef=uncertain_coef, poor_coef=poor_coef, medium_coef=medium_coef, high_coef=high_coef, logger=logger)
end_time = time.time()
p = pstats.Stats('output_file.prof')
p.sort_stats('cumulative').print_stats(10)
execution_time = end_time - start_time
print("Execution time: ", execution_time, "seconds")

# json_data = [trend.to_dict() for trend in rootTrends]
# json_final = json.dumps(json_data)
# with open('trends.json', 'w') as file:
#     file.write(json_final)

save_to_json(rootTrends=rootTrends, filename=filename)