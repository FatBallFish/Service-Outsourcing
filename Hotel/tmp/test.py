import time
from datetime import datetime, timedelta
count_dict = {}
for j in range(24):
    count_dict[j] = j
# count_dict = {0: 1, 5: 3, 8: 4}
data_list = [count_dict[x] for x in count_dict.keys()]
print(data_list)
