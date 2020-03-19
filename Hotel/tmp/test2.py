import time
from datetime import datetime

timestamp = time.time()
time2datetime = datetime.fromtimestamp(timestamp)
print(time2datetime)
print(type(time2datetime))
print(datetime.now())
print(type(datetime.now()))
