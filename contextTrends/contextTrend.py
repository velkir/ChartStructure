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
        self.efficiency = None
        self.status0_when = None
        self.status0_who = None
        self.main = main

    def to_dict(self):
        return {
            'id': self.id,
            'direction': self.direction,
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
            'efficiency': self.efficiency,
            'status0_when': self.status0_when.isoformat() if self.status0_when is not None else None,
            'status0_who': self.status0_who
        }

    def recalculatemaxCorrection(self):
        return self
    def recalculateEfficiency(self):
        return self
    def recalculateStatus(self):
        return self
    def recalculateDelta(self):
        if self.direction == 0:
            self.delta = abs(self.point1/self.point0*100-100)
        elif self.direction == 1:
            self.delta = abs(self.point0/self.point1*100-100)
        return self
    def recalclulateExtremum(self):
        return self



