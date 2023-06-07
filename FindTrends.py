import Data_preprocess
from Trend import Trend

def getTrends(dataframe, minthreshold):
    # df = Data_preprocess.download_ccxt(Market="BTC/USDT", Since='2017-12-11T00:00:00Z', To='2023-08-01T00:00:00Z',Timeframe="1w")
    df = dataframe
    # Минимальная дельта
    # MinThreshold = 0.9
    MinThreshold = minthreshold

    #Сделать параметром от юзера
    Point0 = df.iloc[0]
    # Point0 = point0

    HighPoint = 0
    LowPoint = 0

    #Создаем пустой список трендов
    trends = []

    for bar in range(len(df)):
        #Пропускаем первый бар
        if df.loc[bar, "timestamp"] == Point0["timestamp"]:
            continue

        #Обрабатываем текущую свечу, берем из неё хай и лой
        HighPoint = df.loc[bar, "HIGH"]
        LowPoint = df.loc[bar, "LOW"]
        #Ищем первый тренд
        if len(trends) == 0:
            #Поиск аптренда
            if abs(HighPoint / Point0["LOW"] * 100 - 100) >= MinThreshold * 100 and HighPoint >= Point0["LOW"]:
                print("Найден Аптренд!")
                print(Point0["timestamp"])
                print(df.loc[bar, "timestamp"])
                print(Point0["LOW"])
                print(HighPoint)
                print(abs(HighPoint / Point0["LOW"] * 100 - 100))
                trend = Trend(direction=0, point0=Point0["LOW"], point1=HighPoint, parent=None, status=1,
                              delta=HighPoint / Point0["LOW"] * 100 - 100, timestampstart=Point0["timestamp"],
                              timestampend=df.loc[bar, "timestamp"])
                trends.append(trend)
                continue
            #Поиск даунтренда
            elif abs(LowPoint / Point0["HIGH"] * 100 - 100) >= MinThreshold * 100 and LowPoint <= Point0["HIGH"]:
                print("Найден Даутренд!")
                print(Point0["timestamp"])
                print(df.loc[bar, "timestamp"])
                print(abs(LowPoint / Point0["HIGH"] * 100 - 100))
                trend = Trend(direction=1, point0=Point0["HIGH"], point1=LowPoint, parent=None, status=1,
                              delta=LowPoint / Point0["HIGH"] * 100 - 100, timestampstart=Point0["timestamp"],
                              timestampend=df.loc[bar, "timestamp"])
                trends.append(trend)
                continue
            else:
                if HighPoint >= Point0["LOW"]:
                    print(f"Дельты {abs(HighPoint / Point0['LOW'] * 100 - 100)} недостаточно для аптренда")
                elif LowPoint <= Point0["HIGH"]:
                    print(f"Дельты {abs(LowPoint / Point0['HIGH'] * 100 - 100)} недостаточно для даунтренда")
        #Ищем второй+ тренды
        else:
            #Если текущий тренд - аптренд
            if trends[-1].direction == 0:
                #Если хай текущей свечи выше хая текущего тренда
                if HighPoint > trends[-1].point1:
                    #Переписываем хай тренда
                    trends[-1].point1 = HighPoint
                    trends[-1].timestampend = df.loc[bar, "timestamp"]

                    #Если в этой же свече случается коррекция
                    if (trends[-1].point1 - LowPoint) / (trends[-1].point1 - trends[-1].point0)>=0.382:
                        trend = Trend(direction=1, point0=trends[-1].point1, point1=LowPoint, parent=trends[-1],
                                      status=1, delta=abs(LowPoint/trends[-1].point1*100-100),
                                      timestampstart=trends[-1].timestampend, timestampend=df.loc[bar, "timestamp"])
                        trends.append(trend)
                    continue
                elif (trends[-1].point1 - LowPoint) / (trends[-1].point1 - trends[-1].point0)>=0.382:
                    trend = Trend(direction=1, point0=trends[-1].point1, point1=LowPoint, parent=trends[-1], status=1,
                                  delta=abs(LowPoint/trends[-1].point1*100-100),
                                  timestampstart=trends[-1].timestampend, timestampend=df.loc[bar, "timestamp"])
                    trends.append(trend)
                    continue
            #Если текущий тренд - даунтренд
            if trends[-1].direction == 1:
                #Если лой текущей свечи ниже лоя текущего тренда
                if LowPoint < trends[-1].point1:
                    #Переписываем лой тренда
                    trends[-1].point1 = LowPoint
                    trends[-1].timestampend = df.loc[bar, "timestamp"]

                    if (trends[-1].point1 - HighPoint) / (trends[-1].point1 - trends[-1].point0) >= 0.382:
                        trend = Trend(direction=0, point0=trends[-1].point1, point1=LowPoint, parent=trends[-1],
                                      status=1, delta=abs(HighPoint/trends[-1].point1*100-100),
                                      timestampstart=trends[-1].timestampend, timestampend=df.loc[bar, "timestamp"])
                        trends.append(trend)
                    continue
                elif (trends[-1].point1 - HighPoint) / (trends[-1].point1 - trends[-1].point0) >= 0.382:
                    trend = Trend(direction=0, point0=trends[-1].point1, point1=LowPoint, parent=trends[-1], status=1,
                                  delta=abs(HighPoint/trends[-1].point1*100-100),
                                  timestampstart=trends[-1].timestampend, timestampend=df.loc[bar, "timestamp"])
                    trends.append(trend)
                    continue
    return trends