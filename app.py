from flask import Flask,render_template
import pymysql
from wsgiref.simple_server import make_server
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index')
def index2():
    return render_template("index.html")
    # return index() 也可

@app.route('/movie')
def movie():

    dataList = []
    # 建立连接
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='B19041923',db='spider',charset='utf8')
    # 建立游标,python, 必须有一个游标对象， 用来给数据库发送sql语句， 并执行的.
    cursor = conn.cursor()
    # 4. 关闭游标
    sql = 'select * from movie250'
    result = cursor.execute(sql)
    data = cursor.fetchall()  #查询得到的结果是元组（（1,...）,（2,...））
    for item in data:
        dataList.append(item)
    cursor.close()
    # 5. 关闭连接
    conn.close()
    return render_template("movie.html",movies=dataList)

@app.route('/score')
def score():
    score =[] #评分
    num = [] #每个评分对应的电影数量
    # 建立连接
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='B19041923',db='spider',charset='utf8')
    # 建立游标,python, 必须有一个游标对象， 用来给数据库发送sql语句， 并执行的.
    cursor = conn.cursor()
    # 4. 关闭游标
    sql = 'select score,count(score) from movie250 group by score'
    cursor.execute(sql)
    data = cursor.fetchall()  #查询得到的结果是元组（（1,...）,（2,...））
    for item in data:
        score.append(str(item[0]))
        num.append(item[1])
    cursor.close()
    # 5. 关闭连接
    conn.close()

    return render_template("score.html",score=score,num=num)

@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/word')
def word():
    return render_template("word.html")


if __name__ == '__main__':
    server = make_server('127.0.0.1', 5001, app)
    server.serve_forever()
    app.run()

