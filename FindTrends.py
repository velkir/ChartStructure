from Trend import Trend

def getTrends(dataframe, minthreshold, logger):
    logger.debug('Function getTrends() called')
    df = dataframe
    # Минимальная дельта
    # MinThreshold = 0.9
    MinThreshold = minthreshold

    #Сделать параметром от юзера
    Point0 = df.iloc[0]

    HighPoint = 0
    LowPoint = 0

    mainTrend = None
    rootTrends = []
    firstTrend = True

    for bar in range(len(df)):
        logger.debug('Processing bar number {}'.format(bar))
        #Пропускаем первый бар
        # if df.loc[bar, "timestamp"] == Point0["timestamp"]:
        #     continue
        #Обрабатываем текущую свечу, берем из неё хай и лой
        HighPoint = df.loc[bar, "HIGH"]
        LowPoint = df.loc[bar, "LOW"]
        #Ищем первый тренд
        if firstTrend == True:
            #Поиск аптренда
            if abs(HighPoint / Point0["LOW"] * 100 - 100) >= MinThreshold * 100 and HighPoint >= Point0["LOW"]:
                logger.debug('Found an uptrend: Low={}, High={}'.format(Point0["LOW"], HighPoint))
                trend = Trend(direction=0, point0=Point0["LOW"], point1=HighPoint,
                              delta=HighPoint / Point0["LOW"] * 100 - 100, parent=None, status=1,
                              timestampstart=Point0["timestamp"],
                              timestampend=df.loc[bar, "timestamp"], id=0)
                mainTrend = trend
                logger.debug('Добавляем maintrend с id={} в rootTrends'.format(mainTrend.id))
                rootTrends.append(mainTrend)
                firstTrend=False
                continue
            #Поиск даунтренда
            elif abs(LowPoint / Point0["HIGH"] * 100 - 100  ) >= MinThreshold * 100 and LowPoint <= Point0["HIGH"]:
                logger.debug('Found a downtrend: High={}, Low={}'.format(Point0["HIGH"], LowPoint))
                trend = Trend(direction=1, point0=Point0["HIGH"], point1=LowPoint,
                              delta=LowPoint / Point0["HIGH"] * 100 - 100, parent=None, status=1,
                              timestampstart=Point0["timestamp"],
                              timestampend=df.loc[bar, "timestamp"], id=0)
                mainTrend = trend
                logger.debug('Добавляем maintrend с id={} в rootTrends'.format(mainTrend.id))
                rootTrends.append(mainTrend)
                firstTrend=False
                continue
        #Ищем второй+ тренды
        else:
            # if HighPoint > mainTrend.point1 and LowPoint < mainTrend.point0:
            #     logger.debug('HighPoint is greater than mainTrend.point1 and LowPoint is less than mainTrend.point0')
            #     continue
            #Если текущий тренд - аптренд
            if mainTrend.direction == 0:
                #Если хай текущей свечи выше хая текущего тренда
                if HighPoint > mainTrend.point1:
                    #Переписываем хай тренда
                    logger.debug('Обновляем хай у trend Id:{} с значения {} на значение {}'.format(mainTrend.id, mainTrend.point1, HighPoint))
                    mainTrend.point1 = HighPoint
                    mainTrend.timestampend = df.loc[bar, "timestamp"]
                    if mainTrend.parent != None:
                        logger.debug('Вызываем метод compare_trends (в HighPoint > mainTrend.point1) Parent до вызова: Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1, mainTrend.parent.direction))
                    mainTrend = mainTrend.compare_trends(rootTrends=rootTrends, Highpoint=HighPoint, Lowpoint=LowPoint, logger=logger).last_id()
                    # logger.debug('mainTrendId:{} / lastTrendId:{}'.format(mainTrend.id, get_node_with_max_id(mainTrend).id))

                    if mainTrend.parent != None:
                        logger.debug('Parent после вызова:Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1, mainTrend.parent.direction))
                    continue
                #Если случилась коррекция к уровню 0.618
                elif (mainTrend.point1 - LowPoint) / (mainTrend.point1 - mainTrend.point0)>=0.382:
                    logger.debug('Found a downtrend: High={}, Low={}'.format(mainTrend.point1, LowPoint))
                    trend = Trend(direction=1, point0=mainTrend.point1, point1=LowPoint,
                                  delta=abs(LowPoint / mainTrend.point1 * 100 - 100), parent=mainTrend, status=1,
                                  timestampstart=mainTrend.timestampend, timestampend=df.loc[bar, "timestamp"],
                                  id=mainTrend.id + 1)
                    mainTrend.add_child(trend)
                    mainTrend = trend
                    if mainTrend.parent != None:
                        logger.debug(
                            'Вызываем метод compare_trends (в коррекции аптренда). Parent до вызова: Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0,
                                                                                  mainTrend.parent.point1, mainTrend.parent.direction))
                    mainTrend = mainTrend.compare_trends(rootTrends, Highpoint=HighPoint, Lowpoint=LowPoint, logger=logger).last_id()
                    # logger.debug('mainTrendId:{} / lastTrendId:{}'.format(mainTrend.id, get_node_with_max_id(mainTrend).id))
                    if mainTrend.parent != None:
                        logger.debug(
                            'Parent после вызова:Id:{}, Low:{}, High:{}'.format(mainTrend.parent.id, mainTrend.parent.point0,
                                                                                 mainTrend.parent.point1, mainTrend.parent.direction))
                    continue
            #Если текущий тренд - даунтренд
            if mainTrend.direction == 1:
                #Если лой текущей свечи ниже лоя текущего тренда
                if LowPoint < mainTrend.point1:
                    #Переписываем лой тренда
                    logger.debug('Обновляем лой у trend Id:{} с значения {} на значение {}'.format(mainTrend.id, mainTrend.point1, LowPoint))
                    mainTrend.point1 = LowPoint
                    mainTrend.timestampend = df.loc[bar, "timestamp"]
                    if mainTrend.parent != None:
                        logger.debug('Вызываем метод compare_trends (LowPoint < mainTrend.point1). Parent до вызова: Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1, mainTrend.parent.direction))
                    mainTrend = mainTrend.compare_trends(rootTrends=rootTrends, Highpoint=HighPoint, Lowpoint=LowPoint, logger=logger).last_id()
                    # logger.debug('mainTrendId:{} / lastTrendId:{}'.format(mainTrend.id, get_node_with_max_id(mainTrend).id))
                    if mainTrend.parent != None:
                        logger.debug('Parent после вызова: Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1, mainTrend.parent.direction))
                    continue
                # Если случилась коррекция к уровню 0.618
                elif (mainTrend.point1 - HighPoint) / (mainTrend.point1 - mainTrend.point0) >= 0.382:
                    logger.debug('Found an uptrend: Low={}, High={}'.format(mainTrend.point1, HighPoint))
                    trend = Trend(direction=0, point0=mainTrend.point1, point1=HighPoint,
                                  delta=abs(HighPoint / mainTrend.point1 * 100 - 100), parent=mainTrend, status=1,
                                  timestampstart=mainTrend.timestampend, timestampend=df.loc[bar, "timestamp"],
                                  id=mainTrend.id + 1)
                    mainTrend.add_child(trend)
                    mainTrend = trend
                    if mainTrend.parent != None:
                        logger.debug('Вызываем метод compare_trends (в коррекции шорта): Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1, mainTrend.parent.direction))
                    mainTrend = mainTrend.compare_trends(rootTrends, Highpoint=HighPoint, Lowpoint=LowPoint, logger=logger).last_id()
                    # logger.debug('mainTrendId:{} / lastTrendId:{}'.format(mainTrend.id, get_node_with_max_id(mainTrend).id))
                    if mainTrend.parent != None:
                        logger.debug('Parent после вызова Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0,
                                                                                 mainTrend.parent.point1, mainTrend.parent.direction))
                    continue
    #Что возвращать?
    logger.debug('Function getTrends() completed, returning rootTrends with length {}'.format(len(rootTrends)))
    return rootTrends


