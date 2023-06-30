
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import pymysql


#影片详情链接
findLink = re.compile(r'<a href="(.*?)">')  #创建正则表达式对象，表示匹配规则
#影片图片
#<img width="100" alt="肖申克的救赎" src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp" class="">
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S) #让换行符包含在字符中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating =re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#影片概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)



def getData(baseurl):
    datalist = []
    # 解析数据
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            # print(item) 测试：查看电影item全部信息
            data = []
            item = str(item)
            #影片详情链接
            link = re.findall(findLink,item)[0]
            data.append(link)

            #影片图片
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)

            #影片标题
            titles = re.findall(findTitle,item)
            if(len(titles)==2):   #如果有中英文标题，则分开存储
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","") #去掉无关符号 /The Shawshank Redemption
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')

            #影片评分
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            #影片评价人数
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)

            #影片概述
            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")  #去掉句号
                data.append(inq)
            else:
                data.append(" ")  #留空

            # 影片相关内容
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)  #去掉<br>
            bd = re.sub('/'," ",bd)  #替换
            data.append(bd.strip())  #去掉前后空格

            datalist.append(data) #把处理好的一部电影信息放入datalist中
    return datalist

def saveToMysql(dataList):
    init_db()
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='admin123',db='spider',charset='utf8')
    cursor = conn.cursor()
    for data in dataList:
        for index in range(len(data)):
            if index==4 or index==5:
                continue
            data[index]='"'+data[index]+'"'
        sql='''
                insert into movie250(
                    info_link,pic_link,cname,ename,score,rated,introduce,info)
                    values(%s)'''%",".join(data)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()




def init_db():
    sql='''
        create table movie250(
        id int primary key auto_increment,
        info_link text,
        pic_link text,
        cname varchar(100),
        ename varchar(100),
        score double,
        rated double,
        introduce text,
        info text
        )
    '''
    # 建立连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='admin123',db='spider',charset='utf8')
    # 建立游标,python, 必须有一个游标对象， 用来给数据库发送sql语句， 并执行的.
    cursor = conn.cursor()
    cursor.execute(sql)
    # 4. 关闭游标
    cursor.close()
    # 5. 关闭连接
    conn.close()

def askURL(url):
    head={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    request=urllib.request.Request(url=url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


def main():
    baseurl="https://movie.douban.com/top250?start="
    # 爬取网页
    datalist = getData(baseurl)
    # 保存数据
    saveToMysql(datalist)

if __name__=="__main__":
    main()
    print("爬取完毕")


