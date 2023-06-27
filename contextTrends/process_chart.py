from contextTrend import ContextTrend
import math

contextTrends = []

def process_chart(df, minDelta, contextType, logger):
    def process_first_trend(df, HighPoint, HighPointBar, HighPointTimestamp, LowPoint, LowPointBar, LowPointTimestamp, currentHighPoint, currentLowPoint):
        contextTrend = None
        if currentHighPoint > HighPoint:
            HighPoint = currentHighPoint
            HighPointBar = bar
            HighPointTimestamp = df.loc[bar, "timestamp"]
        if currentLowPoint < LowPoint:
            LowPoint = currentLowPoint
            LowPointBar = bar
            LowPointTimestamp = df.loc[bar, "timestamp"]

        delta = HighPoint / LowPoint * 100 - 100
        if delta>=minDelta:
            if HighPointBar > LowPointBar:
                contextTrend = ContextTrend(id=0, direction=0, point0=LowPoint, point1=HighPoint,
                                            timestamp_point0=LowPointTimestamp, timestamp_point1=HighPointTimestamp,
                                            delta=delta, status=1, main=True)
                contextTrends.append(contextTrend)
            elif HighPointBar < LowPointBar:
                contextTrend = ContextTrend(id=0, direction=1, point0=HighPoint, point1=LowPoint,
                                            timestamp_point0=HighPointTimestamp, timestamp_point1=LowPointTimestamp,
                                            delta=delta, status=1, main=True)
                contextTrends.append(contextTrend)
        return contextTrend, HighPoint, HighPointBar, HighPointTimestamp, LowPoint, LowPointBar, LowPointTimestamp

    def process_trend(df, maincontextTrend, currentHighPoint, currentLowPoint):
        logger.debug('Function process_chart() called')
        if maincontextTrend.direction == 0:
            if currentHighPoint > maincontextTrend.point1:
                if contextType == "inner":
                    if (maincontextTrend.maxCorrection_percent >= 0.298 and maincontextTrend.delta < 500) or (
                            maincontextTrend.maxlogCorrection >= 0.298 and maincontextTrend.delta >= 500):
                        maincontextTrend = maincontextTrend.create_contextTrend_same_direction(df, bar,
                                                                                               currentHighPoint,
                                                                                               currentLowPoint, logger)
                        contextTrends.append(maincontextTrend)
                        maincontextTrend.recalculateEfficiency(contextTrends)
                    else:
                        maincontextTrend.recalclulateExtremum(df, bar, currentHighPoint, currentLowPoint, logger)
                        maincontextTrend.recalculateDelta()
                        maincontextTrend.recalculateEfficiency(contextTrends)
                elif contextType == "outer":
                    if (maincontextTrend.classic_efficiency < 1.5 and maincontextTrend.id != 0) or \
                            ((maincontextTrend.classic_efficiency >= 1.5 or maincontextTrend.id == 0) and (
                                    maincontextTrend.maxCorrection_percent < 0.298 and maincontextTrend.delta < 500) or (
                                     maincontextTrend.maxlogCorrection < 0.298 and maincontextTrend.delta >= 500)):
                        maincontextTrend.recalclulateExtremum(df, bar, currentHighPoint, currentLowPoint, logger)
                        maincontextTrend.recalculateDelta()
                        maincontextTrend.recalculateEfficiency(contextTrends)
                    elif (maincontextTrend.classic_efficiency >= 1.5 and (
                            (maincontextTrend.maxCorrection_percent >= 0.298 and maincontextTrend.delta < 500) or (
                            maincontextTrend.maxlogCorrection >= 0.214 and maincontextTrend.delta >= 500))) or (
                            maincontextTrend.id == 0 and (
                            (maincontextTrend.maxCorrection_percent >= 0.298 and maincontextTrend.delta < 500) or (
                            maincontextTrend.maxlogCorrection >= 0.298 and maincontextTrend.delta >= 500))):
                        maincontextTrend = maincontextTrend.create_contextTrend_same_direction(df, bar,
                                                                                               currentHighPoint,
                                                                                               currentLowPoint,
                                                                                               logger)
                        contextTrends.append(maincontextTrend)
                        maincontextTrend.recalculateEfficiency(contextTrends)
            elif currentLowPoint < maincontextTrend.point0:
                maincontextTrend = maincontextTrend.create_contextTrend_different_direction(df, bar, currentHighPoint, currentLowPoint, logger)
                contextTrends.append(maincontextTrend)
                maincontextTrend.recalculateEfficiency(contextTrends)
            elif maincontextTrend.maxCorrection_price == 0 or maincontextTrend.maxCorrection_price > currentLowPoint:
                maincontextTrend.recalculatemaxCorrection(df, bar, currentHighPoint, currentLowPoint)
            else:
                maincontextTrend.timestampend = df.loc[bar, "timestamp"]
        if maincontextTrend.direction == 1:
            if currentLowPoint < maincontextTrend.point1:
                if contextType == "inner":
                    if (maincontextTrend.maxCorrection_percent >= 0.382 and maincontextTrend.delta < 500) or (
                            maincontextTrend.maxlogCorrection >= 0.382 and maincontextTrend.delta >= 500):
                        maincontextTrend = maincontextTrend.create_contextTrend_same_direction(df, bar,
                                                                                               currentHighPoint,
                                                                                               currentLowPoint, logger)
                        contextTrends.append(maincontextTrend)
                        maincontextTrend.recalculateEfficiency(contextTrends)
                    else:
                        maincontextTrend.recalclulateExtremum(df, bar, currentHighPoint, currentLowPoint, logger)
                        maincontextTrend.recalculateDelta()
                        maincontextTrend.recalculateEfficiency(contextTrends)
                elif contextType == "outer":
                        if (maincontextTrend.classic_efficiency < 1.3 and maincontextTrend.id !=0) or \
                                ((maincontextTrend.classic_efficiency >= 1.3 or maincontextTrend.id == 0) and (maincontextTrend.maxCorrection_percent < 0.382 and maincontextTrend.delta < 500) or (
                                maincontextTrend.maxlogCorrection < 0.382 and maincontextTrend.delta >= 500)):
                            maincontextTrend.recalclulateExtremum(df, bar, currentHighPoint, currentLowPoint, logger)
                            maincontextTrend.recalculateDelta()
                            maincontextTrend.recalculateEfficiency(contextTrends)
                        elif (maincontextTrend.classic_efficiency >= 1.3 and (
                                (maincontextTrend.maxCorrection_percent >= 0.382 and maincontextTrend.delta < 500) or (
                                maincontextTrend.maxlogCorrection >= 0.382 and maincontextTrend.delta >= 500))) or (maincontextTrend.id == 0 and ((maincontextTrend.maxCorrection_percent >= 0.382 and maincontextTrend.delta < 500) or (
                                maincontextTrend.maxlogCorrection >= 0.382 and maincontextTrend.delta >= 500))):
                            maincontextTrend = maincontextTrend.create_contextTrend_same_direction(df, bar,
                                                                                                   currentHighPoint,
                                                                                                   currentLowPoint,
                                                                                                   logger)
                            contextTrends.append(maincontextTrend)
                            maincontextTrend.recalculateEfficiency(contextTrends)
            elif currentHighPoint > maincontextTrend.point0:
                maincontextTrend = maincontextTrend.create_contextTrend_different_direction(df, bar, currentHighPoint, currentLowPoint, logger)
                contextTrends.append(maincontextTrend)
                maincontextTrend.recalculateEfficiency(contextTrends)
            elif currentHighPoint > maincontextTrend.maxCorrection_price:
                maincontextTrend.recalculatemaxCorrection(df, bar, currentHighPoint, currentLowPoint)
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
    LowPointTimestamp = None
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
                                LowPointTimestamp=LowPointTimestamp, currentHighPoint=currentHighPoint, currentLowPoint=currentLowPoint)
        elif len(contextTrends) != 0:
            maincontextTrend = process_trend(df=df, maincontextTrend=maincontextTrend, currentHighPoint=currentHighPoint, currentLowPoint=currentLowPoint)
    return contextTrends