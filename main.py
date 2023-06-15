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

logger, correction_ratio, min_trend_delta, Market, Since, To, Timeframe = Initialization.initialize()

df = download_ccxt(Market=Market, Since=Since, To=To,Timeframe=Timeframe)

start_time = time.time()
# cProfile.run('rootTrends = getTrends(dataframe=df, minthreshold=0.2, logger=logger)', 'output_file.prof')
rootTrends = getTrends(dataframe=df, correction_ratio=correction_ratio, min_trend_delta=min_trend_delta, logger=logger)
end_time = time.time()
p = pstats.Stats('output_file.prof')
p.sort_stats('cumulative').print_stats(10)
execution_time = end_time - start_time
print("Execution time: ", execution_time, "seconds")

save_to_json(rootTrends=rootTrends)