from datetime import datetime

today = datetime.now().date()
date = datetime(2019, 1, 27).date()
cha = today - date
cha = (cha // 365).days
print(cha)
