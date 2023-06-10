class Trend:
    def __init__(self, direction, point0, point1, timestampstart, timestampend, delta, id, parent=None, children=None, status=1):
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
        #status = 0 - inactive
        #status = 1 - active
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'direction': self.direction,
            'point0': self.point0,
            'point1': self.point1,
            'delta': self.delta,
            'parentId': self.parent.id if self.parent is not None else None,
            'children': [child.to_dict() for child in self.children],
            'timestampstart': self.timestampstart.isoformat() if self.timestampstart is not None else None,
            'timestampend': self.timestampend.isoformat() if self.timestampend is not None else None,
            'status': self.status,
        }
    def add_child(self, trend):
        self.children.append(trend)

    def remove_child(self, trend):
        self.children.remove(trend)

    def compare_trends(self, rootTrends, Highpoint, Lowpoint, logger):
        logger.debug(
            'Method compare_trends() called with parameters rootTrends = {}, Highpoint = {}, Lowpoint = {}'.format(
                rootTrends, Highpoint, Lowpoint))
        if self.parent != None:
            if self.parent.parent != None:
                if self.direction != self.parent.direction:
                    if self.parent.direction == 1 and Highpoint > self.parent.point0 or \
                            self.parent.direction == 0 and Lowpoint < self.parent.point0:
                        logger.debug('Setting id:{}, point0:{}, point1:{}, direction:{} status to 0'.format(self.parent.id, self.parent.point0, self.parent.point1, self.parent.direction))
                        self.parent.status = 0
                        # self.parent.status_off_time = self.timestampend
                        logger.debug('Adding child: Id:{} to Id:{}'.format(self.id, self.parent.parent.id))
                        self.parent.parent.add_child(self)
                        logger.debug('Remove child: Id:{} from Id:{}'.format(self.id, self.parent.id))
                        self.parent.remove_child(self)
                        logger.debug('New Parent of Id:{} is Id:{}'.format(self.id, self.parent.parent.id))
                        self.parent = self.parent.parent
                        logger.debug(
                            'Запускаем рекурсивную функцию (изначально была для Id:{}, теперь выполняется для Id:{}'.format(
                                self.id, self.parent.id))
                        return self.parent.compare_trends(rootTrends, Highpoint, Lowpoint, logger=logger)
                elif self.direction == self.parent.direction:
                    logger.debug('Запускаем рекурсивную функцию (изначально была для Id:{}, теперь выполняется для Id:{}'.format(self.id, self.parent.id))
                    return self.parent.compare_trends(rootTrends, Highpoint, Lowpoint, logger=logger)
            elif self.parent.parent == None:
                if self.direction != self.parent.direction:
                    if self.parent.direction == 1 and Highpoint > self.parent.point0 or \
                            self.parent.direction == 0 and Lowpoint < self.parent.point0:
                        logger.debug('Setting id:{}, point0:{}, point1:{}, direction:{} status to 0'.format(self.parent.id, self.parent.point0, self.parent.point1, self.parent.direction))
                        self.parent.status = 0
                        self.parent.status_off_time = self.timestampend
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