import process_chart
from DataSaving import save_to_json
from Data_preprocess import download_ccxt
import Initialization
from Logging import setup_logging
minDelta, Market, Since, To, Timeframe = Initialization.initialize()



df, filename = download_ccxt(Market=Market, Since=Since, To=To,Timeframe=Timeframe)
logger = setup_logging(filename)

context = process_chart.process_chart(df=df, minDelta=minDelta, logger=logger)

save_to_json(rootTrends=context, filename=filename)