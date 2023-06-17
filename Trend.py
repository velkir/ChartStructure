import logging


class Trend:
    all_trends = {}  # словарь для хранения всех экземпляров класса Trend

    def __init__(self, id, direction, point0, point1, timestampstart, timestampend, delta, parent=None, children=None, status=1):
        self.id = id
        #direction = 0 - аптренд
        #direction = 1 - даунтренд
        self.direction = direction
        self.point0 = point0
        self.point1 = point1
        self.delta = delta
        self.parent = parent
        self.children = children if children is not None else []
        self.timestampstart = timestampstart
        self.timestampend = timestampend
        # status = 0 - inactive
        # status = 1 - active
        self.status = status
        self.status0_when = None
        self.status0_who = None
        self.full_delta = delta
        self.efficiency_compare_trends = []
        self.extendedExtremum = point1
        self.extendedExtremum_timestamp = timestampend
        #0 - коррекционное - eff<90%
        #1 - неопреденность - 90%<=eff<110%
        #2 - слабая эффективность - 110%<=eff<150%
        #3 - эффективно - 150%<=eff<500%
        #4 - очень эффективно, дальше не считать - eff>=500%

        #Решил сделать просто процентом
        # добавляем этот экземпляр в словарь all_trends
        Trend.all_trends[id] = self

    @staticmethod
    def get_trend_by_id(trend_id):
        return Trend.all_trends.get(trend_id)

    def to_dict(self):
        return {
            'id': self.id,
            'direction': self.direction,
            'point0': self.point0,
            'point1': self.point1,
            'delta': self.delta,
            'parentId': self.parent.id if self.parent is not None else None,
            'timestampstart': self.timestampstart.isoformat() if self.timestampstart is not None else None,
            'timestampend': self.timestampend.isoformat() if self.timestampend is not None else None,
            'status': self.status,
            'status0_when': self.status0_when.isoformat() if self.status0_when is not None else None,
            'status0_who': self.status0_who if self.status0_who is not None else None,
            'full_delta': self.full_delta,
            'extendedExtremum': self.extendedExtremum,
            'extendedExtremum_timestamp': self.extendedExtremum_timestamp.isoformat() if self.extendedExtremum_timestamp is not None else None,
            'efficiency_compare_trends': [
        {
            'trend': eff_trend.trend.id if eff_trend.trend is not None else None,
            'current_efficiency': eff_trend.current_efficiency,
            'efficiency': {
                'uncertain_efficiency': eff_trend.efficiency.uncertain_efficiency.isoformat() if eff_trend.efficiency.uncertain_efficiency is not None else None,
                'uncertain_efficiency_price': eff_trend.efficiency.uncertain_efficiency_price if not None else None,
                'poor_efficiency': eff_trend.efficiency.poor_efficiency.isoformat() if eff_trend.efficiency.poor_efficiency is not None else None,
                'poor_efficiency_price': eff_trend.efficiency.poor_efficiency_price if not None else None,
                'medium_efficiency': eff_trend.efficiency.medium_efficiency.isoformat() if eff_trend.efficiency.medium_efficiency is not None else None,
                'medium_efficiency_price': eff_trend.efficiency.medium_efficiency_price if not None else None,
                'high_efficiency': eff_trend.efficiency.high_efficiency.isoformat() if eff_trend.efficiency.high_efficiency is not None else None,
                'high_efficiency_price': eff_trend.efficiency.high_efficiency_price if not None else None,
            }
        } for eff_trend in self.efficiency_compare_trends
    ] if self.efficiency_compare_trends else [],
        'children': [child.to_dict() for child in self.children],
    }
    def add_child(self, trend):
        self.children.append(trend)

    def remove_child(self, trend):
        self.children.remove(trend)

    def compare_trends(self, rootTrends, Highpoint, Lowpoint, uncertain_coef, poor_coef, medium_coef, high_coef, logger):
        logger.debug(
            'Method compare_trends() called with parameters rootTrends = {}, Highpoint = {}, Lowpoint = {}'.format(
                rootTrends, Highpoint, Lowpoint))
        if self.parent != None:
            if self.parent.parent != None:
                if self.direction != self.parent.direction:
                    # if self.parent.direction == 1 and Highpoint > self.parent.point0 or \
                    #         self.parent.direction == 0 and Lowpoint < self.parent.point0:
                    if self.parent.direction == 1 and structure_efficiency_high(self, Highpoint) > poor_coef or \
                            self.parent.direction == 0 and structure_efficiency_low(self, Lowpoint) > poor_coef:
                        logger.debug('Setting id:{}, point0:{}, point1:{}, direction:{} status to 0'.format(self.parent.id, self.parent.point0, self.parent.point1, self.parent.direction))
                        self.parent.status = 0
                        self.parent.status0_when = self.last_id().timestampend
                        self.parent.status0_who = self.last_id().id
                        self.add_trend_to_efficiency(trend=self)
                        self.update_efficiency(uncertain_coef, poor_coef, medium_coef, high_coef, logger)
                        logger.debug('Adding child: Id:{} to Id:{}'.format(self.id, self.parent.parent.id))
                        self.parent.parent.add_child(self)
                        logger.debug('Remove child: Id:{} from Id:{}'.format(self.id, self.parent.id))
                        self.parent.remove_child(self)
                        logger.debug('New Parent of Id:{} is Id:{}'.format(self.id, self.parent.parent.id))
                        self.parent = self.parent.parent
                        self.add_trend_to_efficiency(trend=self)
                        self.update_efficiency(uncertain_coef, poor_coef, medium_coef, high_coef, logger)
                        logger.debug(
                            'Запускаем рекурсивную функцию (изначально была для Id:{}, теперь выполняется для Id:{}'.format(
                                self.id, self.parent.id))
                        return self.parent.compare_trends(rootTrends, Highpoint, Lowpoint, uncertain_coef, poor_coef, medium_coef, high_coef, logger=logger)
                elif self.direction == self.parent.direction:
                    logger.debug('Запускаем рекурсивную функцию (изначально была для Id:{}, теперь выполняется для Id:{}'.format(self.id, self.parent.id))
                    return self.parent.compare_trends(rootTrends, Highpoint, Lowpoint, uncertain_coef, poor_coef, medium_coef, high_coef, logger=logger)
            elif self.parent.parent == None:
                if self.direction != self.parent.direction:
                    # if self.parent.direction == 1 and structure_efficiency_high(self, Highpoint) > poor_coef or \
                    #         self.parent.direction == 0 and structure_efficiency_low(self, Lowpoint) > poor_coef:
                    if self.parent.direction == 1 and Highpoint > self.parent.point0 or \
                            self.parent.direction == 0 and Lowpoint < self.parent.point0:
                        logger.debug(
                            'Setting id:{}, point0:{}, point1:{}, direction:{} status to 0'.format(self.parent.id,
                                                                                                   self.parent.point0,
                                                                                                   self.parent.point1,
                                                                                                   self.parent.direction))
                        self.parent.status = 0
                        self.parent.status0_when = self.last_id().timestampend
                        self.parent.status0_who = self.last_id().id
                        logger.debug('Adding mainTrend.id = {} to rootTrends'.format(self.id))
                        rootTrends.append(self)
                        logger.debug('Remove child: Id:{} from Id:{}'.format(self.id, self.parent.id))
                        self.parent.remove_child(self)
                        logger.debug('Setting ex-parent of id:{} to None'.format(self.id))
                        self.parent = None
                        return self
        return self

    def get_root(self):
        while self.parent != None:
            self = self.parent
        return self

    def last_id(self):
        last_id = self
        trends_to_check = [self]

        while trends_to_check:
            current_trend = trends_to_check.pop()
            if current_trend.id > last_id.id:
                last_id = current_trend
            trends_to_check.extend(current_trend.children)
        return last_id

    def get_parent_trends(self):
        parent_trends = []
        current_trend = self.parent
        while current_trend is not None:
            parent_trends.append(current_trend)
            current_trend = current_trend.parent
        return parent_trends

    def get_parent_trends_different_direction(self):
        parent_trends = []
        current_trend = self.parent
        while current_trend is not None:
            if self.direction != current_trend.direction:
                parent_trends.append(current_trend)
            current_trend = current_trend.parent
        return parent_trends

    def get_parent_trends_same_direction(self):
        parent_trends = []
        current_trend = self.parent
        while current_trend is not None:
            if self.direction == current_trend.direction:
                parent_trends.append(current_trend)
            current_trend = current_trend.parent
        return parent_trends
    def recalculate_trend_delta(self):
        if self.direction == 0:
            self.delta = abs(self.point1/self.point0*100-100)
        elif self.direction == 1:
            self.delta = abs(self.point1/self.point0*100-100)
        self.full_delta = self.delta
        self.extendedExtremum_timestamp = self.timestampend
        return self

    def recalculate_parents(self, logger):
        parentTrends = self.get_parent_trends_same_direction()
        if self.direction == 0:
            for parentTrend in range(len(parentTrends)):
                if Trend.get_trend_by_id(parentTrends[parentTrend].id).point1 < self.point1 and Trend.get_trend_by_id(parentTrends[parentTrend].id).extendedExtremum < self.point1:
                    Trend.get_trend_by_id(parentTrends[parentTrend].id).full_delta = abs(self.point1 / parentTrends[parentTrend].point0 * 100 - 100)
                    Trend.get_trend_by_id(parentTrends[parentTrend].id).full_end_date = self.timestampend
                    logger.debug(
                        'Меняем extendedExtremum у Id:{}, direction:{} со значения {} на значение {} из-за тренда Id:{}, direction={}'.format(
                            parentTrends[parentTrend].id, parentTrends[parentTrend].direction,
                            parentTrends[parentTrend].extendedExtremum, self.point1, self.id,
                            self.direction))
                    Trend.get_trend_by_id(parentTrends[parentTrend].id).extendedExtremum = self.point1
                    Trend.get_trend_by_id(parentTrends[parentTrend].id).extendedExtremum_timestamp = self.timestampend
        elif self.direction == 1:
            for parentTrend in range(len(parentTrends)):
                if Trend.get_trend_by_id(parentTrends[parentTrend].id).point1 > self.point1 and Trend.get_trend_by_id(parentTrends[parentTrend].id).extendedExtremum > self.point1:
                    Trend.get_trend_by_id(parentTrends[parentTrend].id).full_delta = abs(self.point1 / parentTrends[parentTrend].point0 * 100 - 100)
                    Trend.get_trend_by_id(parentTrends[parentTrend].id).full_end_date = self.timestampend
                    logger.debug(
                        'Меняем extendedExtremum у Id:{}, direction:{} со значения {} на значение {} из-за тренда Id:{}, direction={}'.format(
                            parentTrends[parentTrend].id, parentTrends[parentTrend].direction,
                            parentTrends[parentTrend].extendedExtremum, self.point1, self.id,
                            self.direction))
                    Trend.get_trend_by_id(parentTrends[parentTrend].id).extendedExtremum = self.point1
                    Trend.get_trend_by_id(parentTrends[parentTrend].id).extendedExtremum_timestamp = self.timestampend
        return self

    # def add_trend_to_efficiency(self, trend, id, efficiency):
    def add_trend_to_efficiency(self, trend):
        self = trend
        if self.parent is not None:
            if self.direction == self.parent.direction:
                self.add_trend_to_efficiency(trend=self.parent)
            elif self.direction != self.parent.direction:
                if not any(eff_trend.trend == self.parent for eff_trend in self.efficiency_compare_trends):
                    # efficiency = self.calculate_efficiency(parent_trend=self.parent)
                    self.efficiency_compare_trends.append(efficiencyTrend(trend=self.parent, current_efficiency=0))
        return self

    def update_efficiency(self, uncertain_coef, poor_coef, medium_coef, high_coef, logger):
        trends = [self]
        parent_trends = self.get_parent_trends_same_direction()
        if parent_trends != None:
            trends.extend(parent_trends)
        for trend in range(len(trends)):
            for eff_trend in trends[trend].efficiency_compare_trends:
                efficiency = trends[trend].calculate_efficiency(trend=trends[trend], parent_trend=eff_trend.trend)
                if efficiency > eff_trend.current_efficiency:
                    logger.debug(
                        'Устанавливаем efficiency для Id:{} относительно Id:{}. Efficiency={}, current_efficiency={}, uncertain_efficiency={}, poor_efficiency={}, medium_efficiency={}, high_efficiency={}, Extremum={}, Extremum_timestamp={}'.format(
                            trends[trend].id, eff_trend.trend.id, efficiency, eff_trend.current_efficiency,
                        eff_trend.efficiency.uncertain_efficiency, eff_trend.efficiency.poor_efficiency,
                        eff_trend.efficiency.medium_efficiency, eff_trend.efficiency.high_efficiency, trends[trend].extendedExtremum, trends[trend].extendedExtremum_timestamp))
                    eff_trend.current_efficiency = efficiency
                    if uncertain_coef < efficiency < poor_coef and eff_trend.efficiency.uncertain_efficiency is None:
                        eff_trend.efficiency.uncertain_efficiency = trends[trend].extendedExtremum_timestamp
                        eff_trend.efficiency.uncertain_efficiency_price = trends[trend].extendedExtremum
                    elif poor_coef < efficiency < medium_coef and eff_trend.efficiency.poor_efficiency is None:
                        eff_trend.efficiency.poor_efficiency = trends[trend].extendedExtremum_timestamp
                        eff_trend.efficiency.poor_efficiency_price = trends[trend].extendedExtremum
                        if eff_trend.efficiency.uncertain_efficiency is None:
                            eff_trend.efficiency.uncertain_efficiency = eff_trend.efficiency.poor_efficiency
                            eff_trend.efficiency.uncertain_efficiency_price = eff_trend.efficiency.poor_efficiency_price
                    elif medium_coef < efficiency < high_coef and eff_trend.efficiency.medium_efficiency is None:
                        eff_trend.efficiency.medium_efficiency = trends[trend].extendedExtremum_timestamp
                        eff_trend.efficiency.medium_efficiency_price = trends[trend].extendedExtremum
                        if eff_trend.efficiency.uncertain_efficiency is None:
                            eff_trend.efficiency.uncertain_efficiency = eff_trend.efficiency.medium_efficiency
                            eff_trend.efficiency.uncertain_efficiency_price = eff_trend.efficiency.medium_efficiency_price
                        if eff_trend.efficiency.poor_efficiency is None:
                            eff_trend.efficiency.poor_efficiency = eff_trend.efficiency.medium_efficiency
                            eff_trend.efficiency.poor_efficiency_price = eff_trend.efficiency.medium_efficiency_price
                    elif efficiency > high_coef and eff_trend.efficiency.high_efficiency is None:
                        eff_trend.efficiency.high_efficiency = trends[trend].extendedExtremum_timestamp
                        eff_trend.efficiency.high_efficiency_price = trends[trend].extendedExtremum
                        if eff_trend.efficiency.uncertain_efficiency is None:
                            eff_trend.efficiency.uncertain_efficiency = eff_trend.efficiency.high_efficiency
                            eff_trend.efficiency.uncertain_efficiency_price = eff_trend.efficiency.high_efficiency_price
                        if eff_trend.efficiency.poor_efficiency is None:
                            eff_trend.efficiency.poor_efficiency = eff_trend.efficiency.high_efficiency
                            eff_trend.efficiency.poor_efficiency_price = eff_trend.efficiency.high_efficiency_price
                        if eff_trend.efficiency.medium_efficiency is None:
                            eff_trend.efficiency.medium_efficiency = eff_trend.efficiency.high_efficiency
                            eff_trend.efficiency.medium_efficiency_price = eff_trend.efficiency.high_efficiency_price

    def calculate_efficiency(self, trend, parent_trend):
        total_movement = abs(parent_trend.point0 - trend.point0)  # общее движение
        current_movement = abs(trend.extendedExtremum - trend.point0)  # текущее движение
        return (current_movement / total_movement)

class efficiencyTrend:
    def __init__(self, trend, current_efficiency):
        self.trend = trend
        self.current_efficiency = current_efficiency
        self.efficiency = Efficiency()

    def to_dict(self):
        return {
            'trend': self.trend.id if self.trend is not None else None,
            'efficiency': self.current_efficiency
        }

class Efficiency:
    def __init__(self):
        self.uncertain_efficiency = None
        self.uncertain_efficiency_price = None
        self.poor_efficiency = None
        self.poor_efficiency_price = None
        self.medium_efficiency = None
        self.medium_efficiency_price = None
        self.high_efficiency = None
        self.high_efficiency_price = None

def structure_efficiency_high(self, Highpoint):
    total_movement_high = abs(self.parent.point0 - self.point0)  # общее движение
    current_movement_high = abs(Highpoint - self.point0)  # текущее движение
    return current_movement_high / total_movement_high

def structure_efficiency_low(self, Lowpoint):
    total_movement_high = abs(self.parent.point0 - self.point0)  # общее движение
    current_movement_high = abs(self.point0 - Lowpoint)  # текущее движение
    return current_movement_high / total_movement_high