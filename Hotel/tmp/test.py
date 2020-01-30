import time
import sys
from datetime import datetime
str = time.mktime(datetime.now().date().timetuple())
print(str)
try:
    timestamp = float(str)
except Exception as e:
    print("is not float")
    sys.exit()
date = time.strftime("%Y-%m-%d", time.localtime(timestamp))
date = datetime.strptime(date, "%Y-%m-%d").date()
print(date)