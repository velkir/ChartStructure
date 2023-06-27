import math

class ContextTrend():
    def __init__(self, id, direction, point0, point1, timestamp_point0, timestamp_point1, delta, main=False, status=1):
        self.id = id
        self.direction = direction
        self.point0 = point0
        self.point1 = point1
        self.main=None
        self.status = status
        self.timestamp_point0 = timestamp_point0
        self.timestamp_point1 = timestamp_point1
        self.timestampend = timestamp_point1
        self.delta = delta
        self.maxCorrection_percent = 0
        self.maxCorrection_price = 0
        self.maxCorrection_timestamp = None
        self.maxlogCorrection = 0
        self.classic_efficiency = 0
        self.log_efficiency = 0
        self.status0_when = None
        self.status0_who = None
        self.main = main

    def to_dict(self):
        return {
            'id': self.id,
            'direction': self.direction,
            'main': self.main,
            'point0': self.point0,
            'point1': self.point1,
            'delta': self.delta,
            'status': self.status,
            'timestamp_point0': self.timestamp_point0.isoformat() if self.timestamp_point0 is not None else None,
            'timestamp_point1': self.timestamp_point1.isoformat() if self.timestamp_point1 is not None else None,
            'timestampend': self.timestampend.isoformat() if self.timestampend is not None else None,
            'maxCorrection_percent': self.maxCorrection_percent,
            'maxCorrection_price': self.maxCorrection_price,
            'maxCorrection_timestamp': self.maxCorrection_timestamp.isoformat() if self.maxCorrection_timestamp is not None else None,
            'maxlogCorrection': self.maxlogCorrection,
            'classic_efficiency': self.classic_efficiency,
            'log_efficiency': self.log_efficiency,
            'status0_when': self.status0_when.isoformat() if self.status0_when is not None else None,
            'status0_who': self.status0_who
        }

    def recalculatemaxCorrection(self, df, bar, currentHighPoint, currentLowPoint):
        if self.direction == 0:
            self.maxCorrection_price = currentLowPoint
            self.maxCorrection_timestamp = df.loc[bar, "timestamp"]
            self.maxCorrection_percent = (self.point1 - currentLowPoint) / (
                    self.point1 - self.point0)
            self.timestampend = df.loc[bar, "timestamp"]
            self.maxlogCorrection = 1 - math.log(currentLowPoint / self.point0) / math.log(
                self.point1 / self.point0)
        elif self.direction == 1:
            self.maxCorrection_price = currentHighPoint
            self.maxCorrection_timestamp = df.loc[bar, "timestamp"]
            self.maxCorrection_percent = (currentHighPoint - self.point1) / (
                    self.point0 - self.point1)
            self.timestampend = df.loc[bar, "timestamp"]
            self.maxlogCorrection = math.log(self.point1 / currentHighPoint) / math.log(
                self.point1 / self.point0)
        return self
    def recalculateEfficiency(self, contextTrends):
        if self.id != 0:
            if self.direction == 0:
                if contextTrends[-2].direction == 0:
                    self.classic_efficiency = abs((self.point1 - self.point0) / (contextTrends[-2].point1 - self.point0))
                    self.log_efficiency = abs(math.log(self.point1 / self.point0) / math.log(contextTrends[-2].point1 / self.point0))
                elif contextTrends[-2].direction == 1:
                    self.classic_efficiency = abs((self.point1 - self.point0) / (contextTrends[-2].point0 - self.point0))
                    self.log_efficiency = abs(math.log(self.point1 / self.point0) / math.log(contextTrends[-2].point0 / self.point0))
            elif self.direction == 1:
                if contextTrends[-2].direction == 0:
                    self.classic_efficiency = abs((self.point0 - self.point1) / (contextTrends[-2].point1 - contextTrends[-2].point0))
                    self.log_efficiency = abs(math.log(self.point0 / self.point1) / math.log(contextTrends[-2].point1 / contextTrends[-2].point0))
                elif contextTrends[-2].direction == 1:
                    self.classic_efficiency = abs((self.point0 - self.point1) / (self.point0 - contextTrends[-2].point1))
                    self.log_efficiency = abs(math.log(self.point0 / self.point1)) / math.log(self.point0 / contextTrends[-2].point1)
            return self


        return self
    def recalculateStatus(self):
        return self
    def recalculateDelta(self):
        if self.direction == 0:
            self.delta = abs(self.point1/self.point0*100-100)
        elif self.direction == 1:
            self.delta = abs(self.point0/self.point1*100-100)
        return self
    def recalclulateExtremum(self, df, bar, currentHighPoint, currentLowPoint, logger):
        if self.direction == 0:
            logger.debug(
                'Коррекция меньше 0.382 ({}) и экстремум ниже хая текущего бара. Экстремум: {}. HighPoint: {}. Обновляем хай'.format(
                    self.maxCorrection_percent, self.point1, currentHighPoint))
            self.point1 = currentHighPoint
            self.timestamp_point1 = df.loc[bar, "timestamp"]
            self.timestampend = self.timestamp_point1
            self.maxCorrection_price = 0
            self.maxCorrection_percent = 0
            self.maxCorrection_timestamp = None
        elif self.direction == 1:
            logger.debug(
                'Коррекция меньше 0.382 ({}) и экстремум выше лоя текущего бара. Экстремум: {}. LowPoint: {}. Обновляем лой'.format(
                    self.maxCorrection_percent, self.point1, currentLowPoint))
            self.point1 = currentLowPoint
            self.timestamp_point1 = df.loc[bar, "timestamp"]
            self.timestampend = self.timestamp_point1
            self.maxCorrection_price = 0
            self.maxCorrection_percent = 0
            self.maxCorrection_timestamp = None
        return self
    def create_contextTrend_same_direction(self, df, bar, currentHighPoint, currentLowPoint, logger):
        if self.direction == 0:
            logger.debug(
                'Коррекция больше 0.382 ({}) и экстремум ниже хая текущего бара. Экстремум: {}. HighPoint: {}. Создаем новый тренд'.format(
                    self.maxCorrection_percent, self.point1, currentHighPoint))
            delta = abs(currentHighPoint / self.maxCorrection_price * 100 - 100)
            contextTrend = ContextTrend(id=self.id + 1, direction=0,
                                        point0=self.maxCorrection_price, point1=currentHighPoint,
                                        timestamp_point0=self.maxCorrection_timestamp,
                                        timestamp_point1=df.loc[bar, "timestamp"],
                                        delta=delta, status=1)
            return contextTrend
        if self.direction == 1:
            logger.debug(
                'Коррекция больше 0.382 ({}) и экстремум ниже хая текущего бара. Экстремум: {}. LowPoint: {}'.format(
                    self.maxCorrection_percent, self.point1, currentLowPoint))
            delta = abs(self.maxCorrection_price / currentLowPoint * 100 - 100)
            contextTrend = ContextTrend(id=self.id + 1, direction=1,
                                        point0=self.maxCorrection_price, point1=currentLowPoint,
                                        timestamp_point0=self.maxCorrection_timestamp,
                                        timestamp_point1=df.loc[bar, "timestamp"],
                                        delta=delta, status=1)
            return contextTrend

    def create_contextTrend_different_direction(self, df, bar, currentHighPoint, currentLowPoint, logger):
        if self.direction == 0:
            logger.debug('currentLowPoint ({})< maincontextTrend.point0 ({}). Создаем даунтренд'.format(currentLowPoint,
                                                                                                        self.point0))
            delta = abs(self.point0 / currentLowPoint * 100 - 100)
            contextTrend = ContextTrend(id=self.id + 1, direction=1, point0=self.point1,
                                        point1=currentLowPoint,
                                        timestamp_point0=self.timestamp_point1,
                                        timestamp_point1=df.loc[bar, "timestamp"],
                                        delta=delta, status=1, main=True)
            return contextTrend
        if self.direction == 1:
            delta = abs(currentHighPoint / self.point0 * 100 - 100)
            contextTrend = ContextTrend(id=self.id + 1, direction=0, point0=self.point1,
                                        point1=currentHighPoint,
                                        timestamp_point0=self.timestamp_point1,
                                        timestamp_point1=df.loc[bar, "timestamp"],
                                        delta=delta, status=1, main=True)
            return contextTrend