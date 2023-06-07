#Long
point0 = 5000
point1 = 13000
LowPoint = 10000


correction_ratio = (point1 - LowPoint) / (point1 - point0)
print(correction_ratio)

#Short
point0 = 13000
point1 = 5000
HighPoint = 9000
correction_ratio = (point1 - HighPoint) / (point1 - point0)
print(correction_ratio)