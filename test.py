from model.DateInfo import DateInfo
from datetime import *

day = datetime.now()

res = DateInfo(day)
print("当前时间：",day)
print("八字计算",res.getBaZi())

