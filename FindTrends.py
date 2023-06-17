from Trend import Trend

def getTrends(dataframe, correction_ratio, min_trend_delta, uncertain_coef, poor_coef, medium_coef, high_coef, logger):
    def process_first_trend(df, bar, HighPoint, LowPoint, Point0, min_trend_delta, rootTrends, logger):
        if abs(HighPoint / Point0["LOW"] * 100 - 100) >= correction_ratio * 100 and HighPoint >= Point0["LOW"]:
            logger.debug('Found an uptrend: Low={}, High={}'.format(Point0["LOW"], HighPoint))
            trend = Trend(direction=0, point0=Point0["LOW"], point1=HighPoint,
                          delta=abs(HighPoint / Point0["LOW"] * 100 - 100), parent=None, status=1,
                          timestampstart=Point0["timestamp"],
                          timestampend=df.loc[bar, "timestamp"], id=0)
            logger.debug('Добавляем maintrend с id={} в rootTrends'.format(trend.id))
            rootTrends.append(trend)
            return trend
        # Поиск даунтренда

        elif abs(LowPoint / Point0["HIGH"] * 100 - 100) >= correction_ratio * 100 and LowPoint <= Point0["HIGH"]:
            logger.debug('Found a downtrend: High={}, Low={}'.format(Point0["HIGH"], LowPoint))
            trend = Trend(direction=1, point0=Point0["HIGH"], point1=LowPoint,
                          delta=abs(LowPoint / Point0["HIGH"] * 100 - 100), parent=None, status=1,
                          timestampstart=Point0["timestamp"],
                          timestampend=df.loc[bar, "timestamp"], id=0)
            logger.debug('Добавляем maintrend с id={} в rootTrends'.format(trend.id))
            rootTrends.append(trend)
            return trend
    def process_trend(mainTrend, correction_ratio, min_trend_delta, uncertain_coef, poor_coef, medium_coef, high_coef):
        def process_uptrend_correction(mainTrend):
            logger.debug('Found a downtrend: High={}, Low={}'.format(mainTrend.point1, LowPoint))
            trend = Trend(direction=1, point0=mainTrend.point1, point1=LowPoint,
                          delta=abs(LowPoint / mainTrend.point1 * 100 - 100), parent=mainTrend, status=1,
                          timestampstart=mainTrend.timestampend, timestampend=df.loc[bar, "timestamp"],
                          id=mainTrend.id + 1)
            mainTrend.add_child(trend)
            mainTrend = trend
            mainTrend = mainTrend.compare_trends(rootTrends=rootTrends, Highpoint=HighPoint, Lowpoint=LowPoint, uncertain_coef=uncertain_coef, poor_coef=poor_coef, medium_coef=medium_coef, high_coef=high_coef,
                                                 logger=logger).last_id()
            mainTrend.add_trend_to_efficiency(mainTrend)
            mainTrend.update_efficiency(uncertain_coef, poor_coef, medium_coef, high_coef, logger)
            mainTrend.recalculate_parents(logger=logger)
            return mainTrend

        def process_downtrend_correction(mainTrend):
            # Если случилась коррекция к уровню 0.618
            logger.debug('Found an uptrend: Low={}, High={}'.format(mainTrend.point1, HighPoint))
            trend = Trend(direction=0, point0=mainTrend.point1, point1=HighPoint,
                          delta=abs(HighPoint / mainTrend.point1 * 100 - 100), parent=mainTrend, status=1,
                          timestampstart=mainTrend.timestampend, timestampend=df.loc[bar, "timestamp"],
                          id=mainTrend.id + 1)
            mainTrend.add_child(trend)
            mainTrend = trend

            if mainTrend.parent != None:
                logger.debug(
                    'Вызываем метод compare_trends (в коррекции шорта): Id:{}, Low:{}, High:{}, Direction:{}'.format(
                        mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1,
                        mainTrend.parent.direction))
            mainTrend = mainTrend.compare_trends(rootTrends=rootTrends, Highpoint=HighPoint, Lowpoint=LowPoint,uncertain_coef=uncertain_coef, poor_coef=poor_coef, medium_coef=medium_coef, high_coef=high_coef,
                                                 logger=logger).last_id()
            mainTrend.add_trend_to_efficiency(mainTrend)
            mainTrend.update_efficiency(uncertain_coef, poor_coef, medium_coef, high_coef, logger)
            mainTrend.recalculate_parents(logger=logger)
            return mainTrend
        def process_uptrend_move_up(mainTrend):
            logger.debug(
                'Обновляем хай у trend Id:{} с значения {} на значение {}'.format(mainTrend.id,
                                                                                  mainTrend.point1,
                                                                                  HighPoint))
            mainTrend.point1 = HighPoint
            mainTrend.recalculate_trend_delta()
            mainTrend.extendedExtremum = mainTrend.point1
            mainTrend.timestampend = df.loc[bar, "timestamp"]
            mainTrend.extendedExtremum_timestamp = mainTrend.timestampend
            mainTrend = mainTrend.compare_trends(rootTrends=rootTrends, Highpoint=HighPoint, Lowpoint=LowPoint,uncertain_coef=uncertain_coef, poor_coef=poor_coef, medium_coef=medium_coef, high_coef=high_coef,
                                                 logger=logger).last_id()
            if mainTrend.id != 0:
                mainTrend.add_trend_to_efficiency(mainTrend)
                mainTrend.update_efficiency(uncertain_coef, poor_coef, medium_coef, high_coef, logger)
            mainTrend.recalculate_parents(logger=logger)
            return mainTrend
        def process_downtrend_move_down(mainTrend):
            mainTrend.point1 = LowPoint
            mainTrend.recalculate_trend_delta()
            mainTrend.extendedExtremum = mainTrend.point1
            mainTrend.timestampend = df.loc[bar, "timestamp"]
            mainTrend.extendedExtremum_timestamp = mainTrend.timestampend
            mainTrend.update_efficiency(uncertain_coef, poor_coef, medium_coef, high_coef, logger)
            if mainTrend.parent != None:
                logger.debug(
                    'Вызываем метод compare_trends (LowPoint < mainTrend.point1). Parent до вызова: Id:{}, Low:{}, High:{}, Direction:{}'.format(
                        mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1,
                        mainTrend.parent.direction))
            mainTrend = mainTrend.compare_trends(rootTrends=rootTrends, Highpoint=HighPoint, Lowpoint=LowPoint,uncertain_coef=uncertain_coef, poor_coef=poor_coef, medium_coef=medium_coef, high_coef=high_coef,
                                                 logger=logger).last_id()
            if mainTrend.id != 0:
                mainTrend.add_trend_to_efficiency(mainTrend)
                mainTrend.update_efficiency(uncertain_coef, poor_coef, medium_coef, high_coef, logger)
            mainTrend = mainTrend.recalculate_parents(logger)
            return mainTrend

        if mainTrend.direction == 0:
            if HighPoint > mainTrend.point1:
                mainTrend = process_uptrend_move_up(mainTrend)
            elif (mainTrend.point1 - LowPoint) / (
                    mainTrend.point1 - mainTrend.point0) >= correction_ratio and mainTrend.point1 / LowPoint * 100 - 100 >= min_trend_delta:
                logger.debug('min_trend_delta={}, correction={}'.format(mainTrend.point1 / LowPoint * 100 - 100,(mainTrend.point1 - LowPoint) / (mainTrend.point1 - mainTrend.point0)))
                mainTrend = process_uptrend_correction(mainTrend)
        elif mainTrend.direction == 1:
            if LowPoint < mainTrend.point1:
                mainTrend = process_downtrend_move_down(mainTrend)
            elif (mainTrend.point1 - HighPoint) / (
                    mainTrend.point1 - mainTrend.point0) >= correction_ratio and HighPoint / mainTrend.point1 * 100 - 100 >= min_trend_delta:
                logger.debug('min_trend_delta={}, correction={}'.format(HighPoint / mainTrend.point1 * 100 - 100,
                                                                        (mainTrend.point1 - HighPoint) / (
                                                                                mainTrend.point1 - mainTrend.point0)))
                mainTrend = process_downtrend_correction(mainTrend)
        return mainTrend

    logger.debug('Function getTrends() called')
    df = dataframe
    # Минимальная дельта
    # MinThreshold = 0.9

    #Сделать параметром от юзера
    Point0 = df.iloc[0]

    HighPoint = 0
    LowPoint = 0

    mainTrend = None
    rootTrends = []
    firstTrend = True

    for bar in range(len(df)):
        logger.debug('Processing bar number {}'.format(bar))
        #Обрабатываем текущую свечу, берем из неё хай и лой
        HighPoint = df.loc[bar, "HIGH"]
        LowPoint = df.loc[bar, "LOW"]
        #Ищем первый тренд

        if firstTrend == True:
            mainTrend = process_first_trend(df, bar, HighPoint, LowPoint, Point0, min_trend_delta, rootTrends, logger)
            if mainTrend != None:
                firstTrend = False
            continue
        #Ищем второй+ тренды
        else:
            mainTrend = process_trend(mainTrend, correction_ratio, min_trend_delta, uncertain_coef, poor_coef, medium_coef, high_coef)

    logger.debug('Function getTrends() completed, returning rootTrends with length {}'.format(len(rootTrends)))
    return rootTrends




    # Ищем второй+ тренды

# def process_high_point(mainTrend, HighPoint, bar, rootTrends, logger):
#     logger.debug('Обновляем хай у trend Id:{} с значения {} на значение {}'.format(mainTrend.id, mainTrend.point1, HighPoint))
#     mainTrend.point1 = HighPoint
#     mainTrend.recalculate_trend_delta()
#     mainTrend.extendedExtremum = mainTrend.point1
#     mainTrend.timestampend = bar["timestamp"]
#     if mainTrend.parent is not None:
#         logger.debug('Вызываем метод compare_trends (в HighPoint > mainTrend.point1) Parent до вызова: Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1, mainTrend.parent.direction))
#     mainTrend = mainTrend.compare_trends(rootTrends=rootTrends, Highpoint=HighPoint, Lowpoint=mainTrend.point1, logger=logger).last_id()
#     if mainTrend.id != 0:
#         mainTrend.update_efficiency()
#     mainTrend = mainTrend.recalculate_parents(logger)
#     if mainTrend.parent is not None:
#         logger.debug('Parent после вызова:Id:{}, Low:{}, High:{}, Direction:{}'.format(mainTrend.parent.id, mainTrend.parent.point0, mainTrend.parent.point1, mainTrend.parent.direction))
#     return mainTrend