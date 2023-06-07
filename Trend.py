class Trend:
    def __init__(self, direction, point0, point1, timestampstart, timestampend, delta, parent=None, status=1):
        #direction = 0 - аптренд
        #direction = 1 - даунтренд
        self.direction = direction
        self.point0 = point0
        self.point1 = point1
        self.delta = delta
        self.parent = parent
        self.timestampstart = timestampstart
        self.timestampend = timestampend
        #status = 0 - inactive
        #status = 1 - active
        self.status = status