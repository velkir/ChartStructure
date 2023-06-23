from contextTrend import ContextTrend
import math

contextTrends = []

def process_chart(df, minDelta, logger):
    def process_first_trend(df, HighPoint, HighPointBar, HighPointTimestamp, LowPoint, LowPointBar, LowPointtTimestamp, currentHighPoint, currentLowPoint):
        contextTrend = None
        if currentHighPoint > HighPoint:
            HighPoint = currentHighPoint
            HighPointBar = bar
            HighPointTimestamp = df.loc[bar, "timestamp"]
        if currentLowPoint < LowPoint:
            LowPoint = currentLowPoint
            LowPointBar = bar
            LowPointtTimestamp = df.loc[bar, "timestamp"]

        delta = HighPoint / LowPoint * 100 - 100
        if delta>=minDelta:
            if HighPointBar > LowPointBar:
                contextTrend = ContextTrend(id=0, direction=0, point0=LowPoint, point1=HighPoint,
                                            timestamp_point0=LowPointtTimestamp, timestamp_point1=HighPointTimestamp,
                                            delta=delta, status=1, main=True)
                contextTrends.append(contextTrend)
            elif HighPointBar < LowPointBar:
                contextTrend = ContextTrend(id=0, direction=1, point0=HighPoint, point1=LowPoint,
                                            timestamp_point0=HighPointTimestamp, timestamp_point1=LowPointtTimestamp,
                                            delta=delta, status=1, main=True)
                contextTrends.append(contextTrend)
        return contextTrend, HighPoint, HighPointBar, HighPointTimestamp, LowPoint, LowPointBar, LowPointtTimestamp

    def process_trend(df, maincontextTrend, currentHighPoint, currentLowPoint):
        logger.debug('Function process_chart() called')
        if maincontextTrend.direction == 0:
            if currentHighPoint > maincontextTrend.point1:
                if (maincontextTrend.maxCorrection_percent >= 0.298 and maincontextTrend.delta < 500) or (maincontextTrend.maxlogCorrection >= 0.298 and maincontextTrend.delta >= 500):
                    logger.debug('Коррекция больше 0.382 ({}) и экстремум ниже хая текущего бара. Экстремум: {}. HighPoint: {}. Создаем новый тренд'.format(maincontextTrend.maxCorrection_percent, maincontextTrend.point1, currentHighPoint))
                    delta = abs(currentHighPoint / maincontextTrend.maxCorrection_price * 100 - 100)
                    contextTrend = ContextTrend(id=maincontextTrend.id + 1, direction=0,
                                                point0=maincontextTrend.maxCorrection_price, point1=currentHighPoint,
                                                timestamp_point0=maincontextTrend.maxCorrection_timestamp,
                                                timestamp_point1=df.loc[bar, "timestamp"],
                                                delta=delta, status=1)
                    contextTrends.append(contextTrend)
                    maincontextTrend = contextTrend
                else:
                    logger.debug('Коррекция меньше 0.382 ({}) и экстремум ниже хая текущего бара. Экстремум: {}. HighPoint: {}. Создаем новый тренд'.format(maincontextTrend.maxCorrection_percent, maincontextTrend.point1, currentHighPoint))
                    maincontextTrend.point1 = currentHighPoint
                    maincontextTrend.timestamp_point1 = df.loc[bar, "timestamp"]
                    maincontextTrend.timestampend = maincontextTrend.timestamp_point1
                    maincontextTrend.maxCorrection_price = 0
                    maincontextTrend.maxCorrection_percent = 0
                    maincontextTrend.maxCorrection_timestamp = None
                    maincontextTrend.recalculateDelta()
                    # recalculate_efficiency
                    # if efficiency >1.5:
                    # maincontextTrend.main = True
            elif currentLowPoint < maincontextTrend.point0:
                logger.debug('currentLowPoint ({})< maincontextTrend.point0 ({}). Создаем даунтренд'.format(currentLowPoint, maincontextTrend.point0))
                delta = abs(maincontextTrend.point0 / currentLowPoint * 100 - 100)
                contextTrend = ContextTrend(id=maincontextTrend.id + 1, direction=1, point0=maincontextTrend.point1,
                                            point1=currentLowPoint,
                                            timestamp_point0=maincontextTrend.timestamp_point1,
                                            timestamp_point1=df.loc[bar, "timestamp"],
                                            delta=delta, status=1, main=True)
                contextTrends.append(contextTrend)
                maincontextTrend = contextTrend
            elif maincontextTrend.maxCorrection_price == 0 or maincontextTrend.maxCorrection_price > currentLowPoint:
                maincontextTrend.maxCorrection_price = currentLowPoint
                maincontextTrend.maxCorrection_timestamp = df.loc[bar, "timestamp"]
                maincontextTrend.maxCorrection_percent = (maincontextTrend.point1 - currentLowPoint) / (
                        maincontextTrend.point1 - maincontextTrend.point0)
                maincontextTrend.timestampend = df.loc[bar, "timestamp"]
                maincontextTrend.maxlogCorrection = 1 - math.log(currentLowPoint / maincontextTrend.point0) / math.log(maincontextTrend.point1 / maincontextTrend.point0)
            else:
                maincontextTrend.timestampend = df.loc[bar, "timestamp"]
        if maincontextTrend.direction == 1:
            if currentLowPoint < maincontextTrend.point1:
                if (maincontextTrend.maxCorrection_percent >= 0.298 and maincontextTrend.delta < 500) or (maincontextTrend.maxlogCorrection >= 0.298 and maincontextTrend.delta >= 500):
                    logger.debug('Коррекция больше 0.382 ({}) и экстремум ниже хая текущего бара. Экстремум: {}. LowPoint: {}'.format(maincontextTrend.maxCorrection_percent, maincontextTrend.point1, currentLowPoint))
                    delta = abs(maincontextTrend.maxCorrection_price / currentLowPoint * 100 - 100)
                    contextTrend = ContextTrend(id=maincontextTrend.id + 1, direction=1,
                                                point0=maincontextTrend.maxCorrection_price, point1=currentLowPoint,
                                                timestamp_point0=maincontextTrend.maxCorrection_timestamp,
                                                timestamp_point1=df.loc[bar, "timestamp"],
                                                delta=delta, status=1)
                    contextTrends.append(contextTrend)
                    maincontextTrend = contextTrend
                else:
                    logger.debug('Коррекция меньше 0.382 ({}) и экстремум выше лоя текущего бара. Экстремум: {}. LowPoint: {}. Создаем новый тренд'.format(maincontextTrend.maxCorrection_percent, maincontextTrend.point1, currentLowPoint))
                    maincontextTrend.point1 = currentLowPoint
                    maincontextTrend.timestamp_point1 = df.loc[bar, "timestamp"]
                    maincontextTrend.timestampend = maincontextTrend.timestamp_point1
                    maincontextTrend.maxCorrection_price = 0
                    maincontextTrend.maxCorrection_percent = 0
                    maincontextTrend.maxCorrection_timestamp = None
                    maincontextTrend.recalculateDelta()
                    # recalculate_efficiency
                    # if efficiency >1.5:
                    # maincontextTrend.main = True
            elif currentHighPoint > maincontextTrend.point0:
                delta = abs(currentHighPoint / maincontextTrend.point0 * 100 - 100)
                contextTrend = ContextTrend(id=maincontextTrend.id + 1, direction=0, point0=maincontextTrend.point1,
                                            point1=currentHighPoint,
                                            timestamp_point0=maincontextTrend.timestamp_point1,
                                            timestamp_point1=df.loc[bar, "timestamp"],
                                            delta=delta, status=1, main=True)
                contextTrends.append(contextTrend)
                maincontextTrend = contextTrend
            elif currentHighPoint > maincontextTrend.maxCorrection_price:
                maincontextTrend.maxCorrection_price = currentHighPoint
                maincontextTrend.maxCorrection_timestamp = df.loc[bar, "timestamp"]
                maincontextTrend.maxCorrection_percent = (currentHighPoint - maincontextTrend.point1) / (
                            maincontextTrend.point0 - maincontextTrend.point1)
                maincontextTrend.timestampend = df.loc[bar, "timestamp"]
                maincontextTrend.maxlogCorrection = math.log(maincontextTrend.point1 / currentHighPoint) / math.log(maincontextTrend.point1 / maincontextTrend.point0)
            else:
                maincontextTrend.timestampend = df.loc[bar, "timestamp"]
        return maincontextTrend


        # def process_move_to_point1()
        #
        # def process_move_to_point0()

    logger.debug('Function process_chart() called')
    HighPoint = 0
    HighPointBar = 0
    HighPointTimestamp = None
    LowPoint = 0
    LowPointBar = 0
    LowPointtTimestamp = None
    maincontextTrend = None

    for bar in range(len(df)):
        logger.debug('Proccesing bar {}'.format(bar))
        currentHighPoint = df.loc[bar, "HIGH"]
        currentLowPoint = df.loc[bar, "LOW"]
        if bar == 0:
            HighPoint = currentHighPoint
            LowPoint = currentLowPoint
        if len(contextTrends) == 0:
            maincontextTrend, HighPoint, HighPointBar, HighPointTimestamp, LowPoint, LowPointBar, LowPointtTimestamp = process_first_trend(df=df, HighPoint=HighPoint, HighPointBar=HighPointBar,
                                HighPointTimestamp=HighPointTimestamp, LowPoint=LowPoint, LowPointBar=LowPointBar,
                                LowPointtTimestamp=LowPointtTimestamp, currentHighPoint=currentHighPoint, currentLowPoint=currentLowPoint)
        elif len(contextTrends) != 0:
            maincontextTrend = process_trend(df=df, maincontextTrend=maincontextTrend, currentHighPoint=currentHighPoint, currentLowPoint=currentLowPoint)
    return contextTrends