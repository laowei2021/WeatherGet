import requests,json
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from PIL import Image
import datetime
   
#中国天气网天津地区地址
url_7day = "https://www.weather.com.cn/weather/"
url_api = "http://t.weather.sojson.com/api/weather/city/"
url_tj_1day = "https://www.weather.com.cn/weather1d/101030100.shtml"
url_tj_7day = "https://www.weather.com.cn/weather/101030100.shtml"
url_tj_api="http://t.weather.sojson.com/api/weather/city/101030100"
#获取网页内容
def get_html(url):
    try:
        #设置请求头
        headers = { 
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' 
	    } 

        reply = requests.get(url,headers=headers,timeout=30)
        
        reply.raise_for_status()
        return reply.content
    except requests.RequestException as e:
        print(e)
        return None

#元素解析并获取天气数据
def parse_html_1day(code):

    #这里使用api，获取更多的信息
    '''
    if not html:
        return {}

    soup = BeautifulSoup(html,"html.parser")

    

    #天气数据
    data = {}

    #城市
    city = soup.find('div',class_="crumbs fl").find('a').text
    data["city"] = city

    #天气
    weather = soup.find('p',class_="wea").title
    data["weather"] = weather

    #温度
    print(soup.find_all('div',class_="tem"))
    temperature = soup.find('div',class_="tem").find(id='span').get_text()
    data["temperature"] = temperature

    #风速风向
    winddir = soup.find('div',class_="zs w").find(id='span').get_text()
    windforce = soup.find('div',class_="zs w").find('em').text
    data["wind"] = f"{winddir} {windforce}"
    
    return data
    '''
    #通过国家气象局api获取天气信息
    weather_dict={}
    reply = requests.get(url_api+str(code))
    d = reply.json()
    #若访问成功，解析天气信息
    if d["status"] == 200:
        weather_dict["city"] = d["cityInfo"]["city"]
        weather_dict["pm25"]=d["data"]["pm25"]
        weather_dict["pm10"]=d["data"]["pm10"]
        weather_dict["weather"] = d["data"]["forecast"][0]["type"]
        weather_dict["high"]=d["data"]["forecast"][0]["high"]
        weather_dict["low"]=d["data"]["forecast"][0]["low"]
        weather_dict["fx"]=d["data"]["forecast"][0]["fx"]
        weather_dict["fl"]=d["data"]["forecast"][0]["fl"]
        weather_dict["moicon"]=d["data"]["shidu"]
        weather_dict["air"]=d["data"]["quality"]
        weather_dict["sunrise"]=d["data"]["forecast"][0]["sunrise"]
        weather_dict["sunset"]=d["data"]["forecast"][0]["sunset"]
        weather_dict["aqi"]=d["data"]["forecast"][0]["aqi"]
        weather_dict["tip"]=d["data"]["forecast"][0]["notice"]

    else:
        return {}
    print(weather_dict)
    return weather_dict

#七日天气情况获取
def parse_html_7day(html):
     if not html:
         return []
     #使用bs4解析网页
     soup = BeautifulSoup(html,"html.parser")

     weatherdata = []
     #解析天气信息
     for item in soup.find_all('li',class_="sky"):
         date = item.find('h1').text
         weather = item.find('p',class_="wea").text
         temperature = item.find('p',class_="tem").find('i').text
         weatherdata.append({"date":date,"weather":weather,"temperature":temperature[:-1]})

     return weatherdata

def get_weeks():
    

    today = datetime.date.today()
    base_year = today.year  # 获取今天的年份
    start_date = datetime.date(base_year-1, 12, 31)  # 设置基准日期为去年的12月31日
    current_date = datetime.date.today()  # 得到今天的时间点

    # 计算从基准日期到今天的时间跨度
    delta = current_date - start_date
    total_days = delta.days  # 获取时间跨度天数

    # 计算星期几（0代表周一）
    week_number = total_days // 7 + 1  # 周一为0，周二是1
    return base_year,week_number

def data_7day_to_image(citycode):
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置字体为黑体
    plt.rcParams['axes.unicode_minus'] = False # 解决负号显示为方块的问题
    plt.figure(figsize=(6.0,5.0))#设置图片尺寸
    plt.xlabel("时间/天")#设置横坐标
    plt.ylabel("温度/摄氏度")#设置纵坐标
    plt.grid(True)#启用网格

    weatherdata=parse_html_7day(get_html(url_7day+str(citycode)+".shtml"))#获取7日数据

    #初始化点数据
    days=[]
    temperatures=[]
    
    #处理点坐标数据
    for i in range(len(weatherdata)):
        days.append(i)
        temperatures.append(int(weatherdata[i]["temperature"]))
    #print(days,temperatures)
    #for i in range(len(days)):
    #    plt.plot(days[i],temperatures[i])
    plt.plot(days,temperatures)#展示点坐标数据
    plt.savefig(".\\tempimages\\file.png")#保存为PNG图片

    year,week = get_weeks()#获取周数数据
 
    image = Image.open(".\\tempimages\\file.png")#转换格式
    image.save(".\\images\\"+str(year)+"-"+str(week)+"-"+str(citycode)+".gif")
    return ".\\images\\"+str(year)+"-"+str(week)+"-"+str(citycode)+".gif"


'''
if __name__ == "__main__":
    #plt.title("TestTemperature")
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置字体为黑体
    plt.rcParams['axes.unicode_minus'] = False # 解决负号显示为方块的问题
    plt.figure(figsize=(6.0,5.0))
    plt.xlabel("时间/天")
    plt.ylabel("温度/摄氏度")
    plt.grid(True)

    weatherdata=parse_html_7day(get_html(url_tj_7day))
    days=[]
    temperatures=[]
    a=[]
    for i in range(len(weatherdata)):
        days.append(i)
        temperatures.append(int(weatherdata[i]["temperature"]))
    print(days,temperatures)
    #for i in range(len(days)):
    #    plt.plot(days[i],temperatures[i])
    plt.plot(days,temperatures)

    plt.savefig(".\\tempimages\\file.png")

    year,week = get_weeks()
    image = Image.open(".\\tempimages\\file.png")
    image.save(".\\images\\"+str(year)+"-"+str(week)+".gif")
    

    plt.show()'
    '''