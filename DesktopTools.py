import DataProcessing as dp
import logging.handlers,logging
import tkinter
import tkinter.messagebox as msg
import tkinter.ttk as ttk
import json
import time
import os
import glob
import PIL
#日志部分 

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
#创建一个StreamHandler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
#创建Formatter
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
#创建TimedRotatingFileHandler
formatted_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

filehandler = logging.handlers.TimedRotatingFileHandler("logs\\"+formatted_time+".log")
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

year,week = dp.get_weeks()
DefaultCityCode = 101010100
dp.data_7day_to_image(DefaultCityCode)



#读取城市代码文件
#cities=[]
pros=[]
pro2 = {}
cities=[]
citydict={}
with open("citycode.json",'r') as f:
    citydict=json.load(f)
    
    for value in range(len(citydict["城市代码"])):

        pros.append(citydict["城市代码"][value]["省"])
        pro2[citydict["城市代码"][value]["省"]]=value
        #for item in value["市"]:
        #    cities.append(item["市名"])

    logger.info("城市代码加载成功")
    
'''
root = tkinter.Tk()
root.geometry()
root.mainloop()
'''
#加载图片文件
def load_icon():
    image_dict={}
    cwd = os.getcwd()
    imagefiles = glob.glob("data\\*")
    for item in imagefiles:
        deitem = item[5:-4]
        image = tkinter.PhotoImage(file=item)
        image_dict[deitem] = image
        logger.info("已加载图片:"+deitem)
    
    return image_dict

#获取当日天气情况
def get_today_weather_inf(code):
    weather = dp.parse_html_1day(code)
    
    
    return weather

#获取7日天气情况
def get_weather_col(code):
    html = dp.get_html(dp.url_7day+str(code)+".shtml")
    pre_weather = dp.parse_html_7day(html)
    weather=[]
    
    for item in pre_weather:
        
        #weather.append(item["date"])
        #weather.append(item["weather"])
        #weather.append(item["temperature"])
        
        weather.append([item["date"],item["weather"],item["temperature"]+'℃'])
    #weather_df = pd.DataFrame(weather, columns=[ "日期","天气", "温度"])
    #print(type(weather_df))
    
    return weather

def province_on_select(event):
    global table
    #print(type(event))
    #print(type(ProvinceComboBox.get()))
    cities=[]
    for item in citydict["城市代码"][pro2[ProvinceComboBox.get()]]["市"]:
        cities.append(item["市名"])
    CityComboBox["value"] = cities
    CityComboBox.current(0)
    CityComboBox.update()


    citycode = citydict["城市代码"][pro2[ProvinceComboBox.get()]]["市"][CityComboBox["value"].index(CityComboBox.get())]["编码"]
    logger.info("城市代码:"+str(citycode))
    new_today = get_today_weather_inf(citycode)
    new_7day = get_weather_col(citycode)
    logger.info("天气信息:"+str(new_today))
    
    if new_7day != None:
        for item in weathertable.get_children():
            weathertable.delete(item)
        for index,data in enumerate(new_7day):
            weathertable.insert('',tkinter.END,values=data)
    weathertable.update()
    logger.info("7日天气数据重载成功")
      
    tablepath = dp.data_7day_to_image(citycode)
    table = tkinter.PhotoImage(file=tablepath)  
    tablelabel.config(image = table)  
    #重新设置天气信息
    #weathericon.set()
    weathericon.config(image = image_dict[new_today["weather"]])
    weatherinfo["text"] = "现在天气:"+new_today["weather"]
    temperature["text"] = "温度 " + new_today["high"] + " " + new_today["low"]
    pm["text"] = "pm2.5:" + str(new_today["pm25"]) + " pm10:" + str(new_today["pm10"])
    wind["text"] = new_today["fx"]+" "+new_today["fl"]
    air["text"] = "空气质量" + " " + str(new_today["aqi"]) + " " + new_today["air"]
    sunrise["text"] = "日出时间 " + new_today["sunrise"]
    sunset["text"] = "日落时间 " + new_today["sunset"]
    moi["text"] = "相对湿度 " + new_today["moicon"]
    notice["text"] = new_today["tip"]

    tablelabel.update()

    weathericon.update()
    weatherinfo.update()
    temperature.update()
    pm.update()
    wind.update()
    air.update()
    sunrise.update()
    sunset.update()
    moi.update()
    notice.update()

    logger.info("天气数据重载成功")


    #root.update()

    

def city_on_select(event):
    global table
    #print(type(event))
    if CityComboBox.get() == None or ProvinceComboBox.get() == None:
        ProvinceComboBox.current(0)
        cities=[]
        for item in citydict["城市代码"][pro2[ProvinceComboBox.get()]]["市"]:
            cities.append(item["市名"])
        CityComboBox["value"]=cities
        CityComboBox.current(0)
        return False
    citycode = citydict["城市代码"][pro2[ProvinceComboBox.get()]]["市"][CityComboBox["value"].index(CityComboBox.get())]["编码"]
    #print(citycode)  
    logger.info("城市代码:"+str(citycode))
    new_today = get_today_weather_inf(citycode)
    new_7day = get_weather_col(citycode)
    '''
    if new_7day or new_today == {}:
        logger.info("无法获取天气信息")
        result = msg.showerror("错误","未提供该区域天气信息")
        print(f"错误:{result}")
    else:
        logger.info("天气信息:"+str(new_today))
    #print(new_today)
    '''
    logger.info("天气信息:"+str(new_today))
    if new_7day != None:
        for item in weathertable.get_children():
            weathertable.delete(item)
        for index,data in enumerate(new_7day):
            weathertable.insert('',tkinter.END,values=data)
    weathertable.update()
    logger.info("7日天气数据重载成功")
 
    tablepath = dp.data_7day_to_image(citycode)
    table = tkinter.PhotoImage(file=tablepath)
    #重新设置天气信息  
    #weathericon.set()
    tablelabel.config(image = table)

    weathericon.config(image = image_dict[new_today["weather"]])
    weatherinfo["text"] = "现在天气:"+new_today["weather"]
    temperature["text"] = "温度 " + new_today["high"] + " " + new_today["low"]
    pm["text"] = "pm2.5:" + str(new_today["pm25"]) + " pm10:" + str(new_today["pm10"])
    wind["text"] = new_today["fx"]+" "+new_today["fl"]
    air["text"] = "空气质量" + " " + str(new_today["aqi"]) + " " + new_today["air"]
    sunrise["text"] = "日出时间 " + new_today["sunrise"]
    sunset["text"] = "日落时间 " + new_today["sunset"]
    moi["text"] = "相对湿度 " + new_today["moicon"]
    notice["text"] = new_today["tip"]

    tablelabel.update()

    weathericon.update()
    weatherinfo.update()
    temperature.update()
    pm.update()
    wind.update()
    air.update()
    sunrise.update()
    sunset.update()
    moi.update()
    notice.update()

    logger.info("天气数据重载成功")
    #root.update()


#创建窗口及配置
root = tkinter.Tk()
root.geometry('1401x500')
root.resizable(0, 0)
#root.attributes('-alpha', 0.4)

image_dict = load_icon()

#
#customstyle = ttk.Style()
#customstyle.configure('Custom.Toplevel',background="#F0F0F0")

#root.attributes("-transparent", "gray")
#设置标题
root.title("天气")

#表格图片加载
table = tkinter.PhotoImage(file=".\\images\\"+str(year)+"-"+str(week)+"-"+str(DefaultCityCode)+".gif")
tablelabel = ttk.Label(root,image=table)
tablelabel.place(x=801,y=5)




weather = get_weather_col(DefaultCityCode)
logger.info("默认城市7日天气数据获取成功")
#7日天气表格
weathertable = ttk.Treeview(root,height=7,columns=["日期","天气","温度"],show='headings')
#label = ttk.Label(root,text=get_weather_col()).pack()
weathertable.heading("日期",text="日期")
weathertable.heading("天气",text="天气")
weathertable.heading("温度",text="温度")

weathertable.column("日期",width=266)
weathertable.column("天气",width=266)
weathertable.column("温度",width=266)

#循环插入数据
for index,data in enumerate(weather):
    weathertable.insert('',tkinter.END,values=data)

weathertable.place(x=0,y=300)
logger.info("7日天气已成功加载")

#获取当日数据
today = get_today_weather_inf(DefaultCityCode)
logger.info("默认城市天气数据获取成功")

#当日天气
ProvinceComboBox = ttk.Combobox(root,value=pros)
ProvinceComboBox.current(0)
ProvinceComboBox.bind('<<ComboboxSelected>>', province_on_select)
ProvinceComboBox.place(x=10,y=5)
logger.info("省份加载成功")

for item in citydict["城市代码"][pro2[ProvinceComboBox.get()]]["市"]:
    cities.append(item["市名"])
CityComboBox = ttk.Combobox(root,value=cities)
CityComboBox.current(0)
CityComboBox.bind('<<ComboboxSelected>>', city_on_select)
CityComboBox.place(x=300,y=5)
logger.info("城市加载成功")

#city = ttk.Label(root,text=today["city"]+"天气",font=("黑体",15)).place(x=10,y=5)
weathericon = ttk.Label(root,image=image_dict[today["weather"]]);weathericon.place(x=0,y=40)
weatherinfo = ttk.Label(root,text="现在天气:"+today["weather"],font=("黑体",20));weatherinfo.place(x=91,y=55)
temperature = ttk.Label(root,text="温度"+" "+today["high"]+" "+today["low"],font=("黑体",15));temperature.place(x=91,y=95)
pm = ttk.Label(root,text="pm2.5:"+str(today["pm25"])+" "+"pm10:"+str(today["pm10"]),font=("黑体",15));pm.place(x=91,y=131)
wind = ttk.Label(root,text=today["fx"]+" "+today["fl"],font=("黑体",15));wind.place(x=91,y=171)
sevendays = ttk.Label(root,text="七日天气预报",font=("黑体",15)).place(x=5,y=256)

air = ttk.Label(root,text="空气质量" + " " + str(today["aqi"]) + " " + today["air"],font=("黑体",15));air.place(x=450,y=55)
sunrise = ttk.Label(root,text="日出时间" + " " + today["sunrise"],font=("黑体",15));sunrise.place(x=450,y=90)
sunset = ttk.Label(root,text="日落时间" + " " + today["sunset"],font=("黑体",15));sunset.place(x=450,y=120)
moi = ttk.Label(root,text="相对湿度" + " " + today["moicon"],font=("黑体",15));moi.place(x=450,y=150)
notice = ttk.Label(root,text=today["tip"],font=("黑体",10));notice.place(x=450,y=185)
logger.info("单日天气基本控件加载成功")

root.mainloop()