import json
from datetime import *
import requests
BASE_URL = "https://www.rili.com.cn/rili/json/pc_wnl/"
TIAN_GAN = "甲乙丙丁戊己庚辛壬癸"
DI_ZHI = "子丑寅卯辰巳午未申酉戌亥"


class DateInfo:
    def __init__(self, date:datetime):
        self.date = date
        self.url = BASE_URL + str(self.date.year)+"/"+str(self.date.month)+".js"
        self.dateStr = requests.get(self.url).text
        self.res = json.loads(self.dateStr.split('jsonrun_PcWnl(')[1]
                       .replace('\\n','\n')
                       .split(',"js");')[0])
        self.dateinfos = self.res['data']
        self.today = self.getToday()
        self.nianzhu = self.today['gz_nian']
        self.yuezhu =  self.today['gz_yue']
        self.rizhu = self.today['gz_ri']
        index = (self.date.hour % 23 + 1)//2
        self.shizhu = TIAN_GAN[(TIAN_GAN.index(self.rizhu[0])%5*2+index)%10]+DI_ZHI[index]
    
    def getToday(self):
        for dateinfo in self.dateinfos:
            if dateinfo['yuethis'] == 0 and dateinfo['ri'] == self.date.day:
                return dateinfo
        return None

    def getBaZi(self):
        return self.nianzhu + self.yuezhu + self.rizhu + self.shizhu