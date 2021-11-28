from flask import Flask,request,url_for,render_template,redirect
import pymysql

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

# 获取登录参数及处理
@app.route('/login',methods=['GET','POST'])
def getLoginRequest():
    # 连接数据库
    db = pymysql.connect(host="localhost", user="root", password="123456", db="student",charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
        # 执行sql语句
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("select * from user where username= '%s' and password= '%s'" % \
                   (username,password))
    results = cursor.fetchall()
    print(results)
    if len(results) == 1:
        return render_template('index.html')
    else:
        return '用户名或密码不正确'
        # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
    # 连接数据库
        db = pymysql.connect(host="localhost", user="root", password="123456", db="student",charset='utf8')
    # 使用cursor()方法获取操作游标
        cursor = db.cursor()
    # 执行sql语句
        username = request.form.get('username')
        password = request.form.get('password')
        x = cursor.execute("select * from user where username = '%s'" %(username))
        print(x)
        db.commit()
        result = cursor.fetchall()
        print(len(result))
        if len(result) == 1:
            return "用户名已经存在"
        else:
            try:
                sql = "insert into user(username,password) values(%s,%s)"
                values = (username,password)
                cursor.execute(sql,values)
                results = cursor.fetchall()
                print(results)
                if len(results) == 0:
                    db.commit()
                    return render_template('login.html')
            except Exception as e:
                    return print("发生异常了"+e)
        return render_template('register.html')
    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/addstu',methods=['GET','POST'])               #这里是添加模块
def addstu():
    if request.method=='POST':
        db = pymysql.connect(host="localhost", user="root", password="123456", db="student",charset='utf8')
        cursor = db.cursor()
        number = request.form.get('number')
        x = cursor.execute("select * from student where number = %s " %(number))  #用输入的学号查询数据库是否有数据
        print(x)
        db.commit()
        result = cursor.fetchall()
        print(len(result))
        if len(result) == 1:
            return "学生已经存在"
        else:
            sql = "insert into student(name,age,sex,number,java,python,network) values(%s,%s,%s,%s,%s,%s,%s)"
            name = request.form.get('name')
            age = request.form.get('age')
            sex = request.form.get('sex')
            java = request.form.get('java')
            python = request.form.get('python')
            network = request.form.get('network')
            values = (name, age, sex, number, java, python,network)
            print(values)
            try:
                results = cursor.execute(sql, values)
                print(results)
                if results==1:
                    db.commit()
                    return "添加成功"
                else:
                    return "添加失败"
            except Exception as e:
                print("发生异常了，异常如下：")
                print(e)
        db.close()
        return render_template('addstu.html')
    return render_template('addstu.html')                     #添加成功则重定向到首页

@app.route('/delstu',methods=['GET','POST'])               #这里是删除模块，对应的页面是/delstu
def delstu():
    if request.method == 'POST':
        db = pymysql.connect(host="localhost", user="root", password="123456", db="student",charset='utf8')
        cursor = db.cursor()
        number = request.form.get('number')
        # print(number) //调式用，查看输入的学号值
        x = cursor.execute("select * from student where number = %s " %(number))
        # print(x)      //调式用，查看数据库查询的结果
        results = cursor.fetchall()
        print(results)
        if len(results) == 1:
            try:
                cursor.execute("delete from student where number = %s" %(number))
                db.commit()
            except:
                db.rollback()
            return "删除成功"
        else:
            return "学生不存在，请重新输入"
        return render_template('delstu.html')
        db.close()
    return render_template('delstu.html')

@app.route('/altstu',methods=['GET','POST'])                  #这里是修改模块，先要找到要修改的学号，如果找到了进行操作
def altstu():
    if request.method=='POST':
        number = request.form.get('number')
        java = request.form.get('java')
        python = request.form.get('python')
        network = request.form.get('network')
        db = pymysql.connect(host="localhost", user="root", password="123456", db="student", charset='utf8')
        cursor = db.cursor()
        javasql = "update student set java=%s where number =%s" %(java,number)
        pythonsql = "update student set python=%s where number =%s" % (python, number)
        networksql = "update student set network=%s where number =%s" % (network, number)
        if (len(java)==0 & len(python)==0 & len(network)==0):
            return '亲，请至少输入一个要修改的分数哦'
        else:
            try:
                if(java != ""):
                    cursor.execute(javasql)
                if(python != ""):
                    cursor.execute(pythonsql)
                if(network != ""):
                    cursor.execute(networksql)
                db.commit()
                return "修改成功 当前修改了java分数："+java+",python分数："+python+",network分数："+network
            except Exception as e:
                print('发生异常了 异常如下')
                print(e)
        db.close()
        return render_template('altstu.html')
    return render_template('altstu.html')

@app.route('/searchstu',methods=['GET','POST'])
def searchstu():
    if request.method=='POST':
        number = request.form.get('number')
        db = pymysql.connect(host="localhost", user="root", password="123456", db="student", charset='utf8')
        cursor = db.cursor()
        sql = "select * from student where number = %s " %(number)
        if(len(number)==0):
            return render_template('searchstu.html',a='亲未输入学号哦')
        else:
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            if len(results)==1:
                return render_template('searchstu.html',results=results)
            else:
                return render_template('searchstu.html',results='没有这个学生哦，请重新输入')
        db.close()
    return render_template('searchstu.html')

@app.route('/searchallstu',methods=['GET','POST'])
def searchallstu():
    if request.method == 'POST':
        db = pymysql.connect(host="localhost", user="root", password="123456", db="student", charset='utf8')
        cursor = db.cursor()
        sql = "select * from student"
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        return render_template('searchallstu.html', results=results)
        db.close()
    return render_template('searchallstu.html')

if __name__ == '__main__':
    app.run() #启动项目,默认端口5000