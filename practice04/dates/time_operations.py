import datetime

d1 = datetime.datetime(2024, 1, 1)
d2 = datetime.datetime.now()

diff = d2 - d1
print(diff.days)
