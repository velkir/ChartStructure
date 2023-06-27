import process_chart
from DataSaving import save_to_json
from Data_preprocess import download_ccxt
import Initialization
from Logging import setup_logging
minDelta, Market, Since, To, Timeframe = Initialization.initialize()
import ccxt


df, filename = download_ccxt(Market=Market, Since=Since, To=To,Timeframe=Timeframe, Exchange=ccxt.binance())
logger = setup_logging(filename)

context = process_chart.process_chart(df=df, minDelta=minDelta, logger=logger, contextType="outer")

save_to_json(rootTrends=context, filename=filename)