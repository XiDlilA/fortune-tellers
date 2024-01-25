import json
from datetime import *
import requests
from rich.text import Text
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console

BASE_URL:str = "https://www.rili.com.cn/rili/json/pc_wnl/"
TIAN_GAN:str = "甲乙丙丁戊己庚辛壬癸"
DI_ZHI:str = "子丑寅卯辰巳午未申酉戌亥"

class API():
    def __init__(self):
        self.datainfo = None
        pass
    
    def today(self):
        console = Console()
        self.datainfo = DateInfo(datetime.now())
        
        title_good = Text("宜", style="bold green")
        panel_good = Panel(Text('\n\n'+'\n\n'.join(self.datainfo.today['yi']), style="bold green", justify='center'),title=title_good, subtitle=title_good, border_style="green", height=30)
        
        title_bad = Text("忌", style="bold red")
        panel_bad = Panel(Text('\n\n'+'\n\n'.join(self.datainfo.today['ji']), style="bold red", justify='center'),title=title_bad, subtitle=title_bad, border_style="red", height=30)
        
        title_info = Text(str(self.datainfo.date), style="bold")
        subtitle_info = Text(self.datainfo.lunar_calendar, style="bold")
        text_info_buddha = Text("\n _ooOoo_\n o8888888o\n 88\" . \"88 \n (| -_- |)  \n O\  =  /O\n ____/`---'\____\n.'  \\|     |//  `.\n/  \\|||  :  |||//  \\\n/  _||||| -:- |||||-  \\\n|   | \\\  -  /// |   |\n| \_|  ''\---/''  |   |\n\  .-\__  `-`  ___/-. /\n___`. .'  /--.--\  `. . __\n.\"\" '<  `.___\_<|>_/___.'  >'\"\".\n| | :  `- \`.;`\ _ /`;.`/ - ` : | |\n\  \ `-.   \_ __\ /__ _/   .-` /  /\n=====`-.____`-.___\_____/___.-`____.-'======\n`=---='\n", style="yellow", justify='center')
        panel_info_buddha = Panel(text_info_buddha,title=title_info, subtitle=subtitle_info, border_style="yellow", width=60, height=21)
        
        title_info_body = Text(self.datainfo.sign + " 第"+str(self.datainfo.today['week'])+"周"+self.datainfo.today['ddd'], justify='center', style="blue bold")
        subtitle_info_body = Text(self.datainfo.bazi, style="bold")
        text_info_body_solar_terms_days = Text("\n"+self.datainfo.solar_terms_days+"\n", style="bold", justify='center')
        text_info_body_solar_terms = Text(self.datainfo.solar_terms, style="bold", justify='center')
        
        panel_info_body = Panel(text_info_body_solar_terms_days+text_info_body_solar_terms, border_style="blue", title=title_info_body, subtitle = subtitle_info_body, height=9, width=60)
        
        
        layout = Layout()
        layout_body = Layout(size=60,name="body")
        layout_body.split_column(
            Layout(panel_info_buddha,size=21),
            Layout(panel_info_body,size=9)
        )
        layout.split_row(
            Layout(panel_good, size=15),
            layout_body,
            Layout(panel_bad, size=15)
        )
        console.print(layout)

    
class DateInfo:
    def __init__(self, date:datetime):
        self.date = date
        self.url = BASE_URL + str(self.date.year)+"/"+str(self.date.month)+".js"
        self.dateStr = requests.get(self.url).text
        self.res = json.loads(self.dateStr.split('jsonrun_PcWnl(')[1]
                       .replace('\\n','\n')
                       .split(',"js");')[0])
        self.dateinfos = self.res['data']
        self.today = self.getTodayInfo()
        self.nianzhu = self.today['gz_nian']
        self.yuezhu =  self.today['gz_yue']
        self.rizhu = self.today['gz_ri']
        index = (self.date.hour % 23 + 1)//2
        self.shizhu = TIAN_GAN[(TIAN_GAN.index(self.rizhu[0])%5*2+index)%10]+DI_ZHI[index]
        self.bazi = self.nianzhu + self.yuezhu + self.rizhu + self.shizhu
        self.lunar_calendar = self.today['shengxiao'] + '年' +self.today['jj_key'] + " " + self.today['n_yueri']
        self.solar_terms_days = str(self.today['jieqi_pass']) + "天 <=-=-=-=-=> " +\
                            str(self.today['jieqi_next']) + '天'
        self.solar_terms = self.today['jieqi'] + " <---------> 今天 <---------> " \
                            + self.today['jieqi_next_link'].split('>')[1].split('<')[0]
        self.sign = self.today['xingzuo_link'].split('>')[1].split('<')[0]
    def getTodayInfo(self):
        for dateinfo in self.dateinfos:
            if dateinfo['yuethis'] == 0 and dateinfo['ri'] == self.date.day:
                return dateinfo
        return None
    
    def getColorfulBaZi(self):
        return "[blue]" + self.nianzhu + \
               "[green]" + self.yuezhu + \
               "[red]" + self.rizhu + \
               "[yellow]" + self.shizhu