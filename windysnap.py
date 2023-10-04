import datetime
import time
from pydoc import html

from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import pymysql
from selenium import webdriver
from decimal import *

from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
#庄河沿岸
#https://www.oceanguide.org.cn/NearshoreForecast?name=N02
#皮口沿岸
#https://www.oceanguide.org.cn/NearshoreForecast?name=N03
#外长山海域
#https://www.oceanguide.org.cn/NearshoreForecast?name=N05
#金州东近海
#https://www.oceanguide.org.cn/NearshoreForecast?name=N06
#大连湾
#https://www.oceanguide.org.cn/NearshoreForecast?name=N07
#付家庄老虎滩海域
#https://www.oceanguide.org.cn/NearshoreForecast?name=N08
#旅顺海域
#https://www.oceanguide.org.cn/NearshoreForecast?name=N09

todayDate = datetime.date.today()

print("完整日期",datetime.date.today())
print("年份",todayDate.year)
print("月份",todayDate.month)
print("日期",todayDate.day)
print("完整日期",str(todayDate.year)+str(todayDate.month)+str(todayDate.day))

# 列表数据登录进数据库
def saveToMysql(dataList):
    conn = pymysql.connect(host='124.223.23.177', port=3306, user='root', passwd='Fish666',db='fish_weather',charset='utf8')
    cursor = conn.cursor()
    # delte the existing data
    delSql = 'delete from sea_temperature where data_date=%s'
    print(delSql)
    cursor.execute(delSql,str(todayDate))
    # insert data
    for data in dataList:
        sql = 'insert into sea_temperature(spot_id,data_date,low_temp,high_temp) VALUES (%s,%s,%s,%s)'
        print(sql)
        cursor.execute(sql, (data[2], str(todayDate), data[0], data[1]))

    conn.commit()
    cursor.close()
    conn.close()

# 取得城市列表
spotdic = {'02':'http://www.oceanguide.org.cn/NearshoreForecast?name=N02', # 庄河附近
          '03':'http://www.oceanguide.org.cn/NearshoreForecast?name=N03', # 皮口
          '05':'http://www.oceanguide.org.cn/NearshoreForecast?name=N05', # 獐子岛
          '06':'http://www.oceanguide.org.cn/NearshoreForecast?name=N06', # 金州
          '07':'http://www.oceanguide.org.cn/NearshoreForecast?name=N07', # 大连湾
          '08':'http://www.oceanguide.org.cn/NearshoreForecast?name=N08', # 三山岛 付家庄
          '09':'http://www.oceanguide.org.cn/NearshoreForecast?name=N09', # 旅顺东
          '10':'http://www.oceanguide.org.cn/NearshoreForecast?name=N10'} # 旅顺西部


# for ubuntu server
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox') # 这个配置很重要
client = webdriver.Chrome(chrome_options=chrome_options, executable_path='/usr/bin/chromedriver')    #

# for windows client
#client = webdriver.Chrome()

tempList = []

for key in spotdic:
    print(key, ":", spotdic[key])
    client.get(spotdic[key])
    time.sleep(4)
    element = client.find_element(By.XPATH, "/html/body/div/section/main/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/table/tr[2]/td[2]")
    print(element.text)
    itemList = []
    str_pat = re.compile(r'[\d]+[.]?[\d]*')
    itemList = str_pat.findall(element.text)
    itemList.append(key)
    print(itemList)
    tempList.append(itemList)

print(len(tempList))
for data in tempList:
    print(data[0])
    print(data[1])
    print(data[2])

saveToMysql(tempList)

# 循环列表取得温度更新列表
