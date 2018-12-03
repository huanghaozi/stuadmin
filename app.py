# -- coding:utf8 --
from flask import Flask, render_template, redirect, session, request
import pymysql, json, db
import datetime

app = Flask(__name__)

app.secret_key = 'littlepossiblilitytobecracked'
database = pymysql.connect("localhost", "root", "123456", "stuadmin")


class dateJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


# ---------------错误处理---------------
@app.errorhandler(404)
def miss(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error500(e):
    return render_template('500.html'), 500


# ---------------end----------------
def auth(func):
    def inner(*args, **kwargs):
        uname = session.get('username')
        if not uname:
            session['logged2pages'] = 'False'
            return redirect('/')
        session['logged2pages'] = 'True'
        return func(*args, **kwargs)

    return inner


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        if session.get('logged2pages') == 'False':
            return render_template('login.html', msg='请先登陆')
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'demo' and password == 'demo':
            session['username'] = username
            return redirect('/department')
        return render_template('login.html', msg='用户名或密码错误')


@app.route('/department', methods=['GET', 'POST'], endpoint='department')
@auth
def department():
    return render_template('department.html')


@app.route('/class', methods=['GET', 'POST'], endpoint='classes')
@auth
def classes():
    return render_template('class.html')


@app.route('/student', methods=['GET', 'POST'], endpoint='student')
@auth
def student():
    return render_template('student.html')


@app.route('/search', methods=['GET', 'POST'], endpoint='search')
@auth
def search():
    return render_template('search.html')


@app.route('/change', methods=['GET', 'POST'], endpoint='change')
@auth
def change():
    return render_template('change.html')


@app.route('/static/changes.html', methods=['GET', 'POST'], endpoint='changesiframe')
@auth
def changesiframe():
    return render_template('changes.html')


@app.route('/static/rewards.html', methods=['GET', 'POST'], endpoint='rewardsiframe')
@auth
def changesiframe():
    return render_template('rewards.html')


@app.route('/static/punishes.html', methods=['GET', 'POST'], endpoint='punishesiframe')
@auth
def changesiframe():
    return render_template('punishes.html')


@app.route('/reward', methods=['GET', 'POST'], endpoint='reward')
@auth
def reward():
    return render_template('reward.html')


@app.route('/punish', methods=['GET', 'POST'], endpoint='punish')
@auth
def punish():
    return render_template('punish.html')


@app.route('/depadata', methods=['GET'], endpoint='depadata')
@auth
def depadata():
    datas = db.gettable(database, 'department', ['departid', 'departname', 'departhead', 'telephone'])
    return json.dumps({"result": "success", "data": datas, "message": "未知错误",
                       "pager": {"page": 1, "recTotal": 1001, "recPerPage": 10}})


@app.route('/classdata', methods=['GET'], endpoint='classdata')
@auth
def classdata():
    datas = db.gettable(database, 'class', ['classid', 'classname', 'departid', 'begindate', 'master', 'mastertel'])
    return json.dumps({"result": "success", "data": datas, "message": "未知错误",
                       "pager": {"page": 1, "recTotal": 1001, "recPerPage": 10}}, cls=dateJsonEncoder)


@app.route('/studata', methods=['GET'], endpoint='studata')
@auth
def studata():
    datas = db.gettable(database, 'student', ['studentid', 'name', 'sex', 'classid', 'birthday', 'native'])
    return json.dumps({"result": "success", "data": datas, "message": "未知错误",
                       "pager": {"page": 1, "recTotal": 1001, "recPerPage": 10}}, cls=dateJsonEncoder)


@app.route('/changedata', methods=['GET'], endpoint='changedata')
@auth
def changedata():
    datas = db.gettable(database, 'changes', ['cid', 'changess', 'recdate', 'studentid'])
    return json.dumps({"result": "success", "data": datas, "message": "未知错误",
                       "pager": {"page": 1, "recTotal": 1001, "recPerPage": 10}}, cls=dateJsonEncoder)


@app.route('/rewarddata', methods=['GET'], endpoint='rewarddata')
@auth
def rewarddata():
    datas = db.gettable(database, 'reward', ['rid', 'studentid', 'reward', 'recdate'])
    return json.dumps({"result": "success", "data": datas, "message": "未知错误",
                       "pager": {"page": 1, "recTotal": 1001, "recPerPage": 10}}, cls=dateJsonEncoder)


@app.route('/punishdata', methods=['GET'], endpoint='punishdata')
@auth
def punishdata():
    datas = db.gettable(database, 'punish', ['pid', 'studentid', 'punish', 'recdate'])
    return json.dumps({"result": "success", "data": datas, "message": "未知错误",
                       "pager": {"page": 1, "recTotal": 1001, "recPerPage": 10}}, cls=dateJsonEncoder)


if __name__ == '__main__':
    app.run()
