# -- coding:utf8 --
from flask import Flask, render_template, redirect, session, request
from DBUtils import PooledDB
import pymysql, json, db
import datetime

app = Flask(__name__)
app.secret_key = 'littlepossiblilitytobecracked'
pool = PooledDB.PooledDB(pymysql, 50, host='localhost', user='root', passwd='123456', db='stuadmin', port=3306)

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

@app.route('/fonts/zenicon.woff')
def zenIconWoff():
    return redirect('/static/fonts/zenicon.woff')

@app.route('/fonts/zenicon.ttf')
def zenIconTTF():
    return redirect('/static/fonts/zenicon.ttf')


@app.route('/fonts/zenicon.eot')
def zenIconEOT():
    return redirect('/static/fonts/zenicon.eot')


@app.route('/fonts/zenicon.svg')
def zenIconSVG():
    return redirect('/static/fonts/zenicon.svg')

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
    if request.method == 'GET':
        return render_template('department.html')
    else:
        if request.form.get('posttype') == 'insert':
            numi = request.form.get('numi')
            newdepanum = []
            newdepaname = []
            newhead = []
            newtele = []
            newdatasets = "("
            for i in range(int(numi)):
                newdepanum.append(request.form.get('newdepanum' + str(i + 1)))
                newdepaname.append(request.form.get('newdepaname' + str(i + 1)))
                newhead.append(request.form.get('newhead' + str(i + 1)))
                newtele.append(request.form.get('newtele' + str(i + 1)))
            for i in range(int(numi)):
                newdatasets += '"' + newdepanum[i] + '",'
                newdatasets += '"' + newdepaname[i] + '",'
                newdatasets += '"' + newhead[i] + '",'
                newdatasets += '"' + newtele[i] + '"'
                newdatasets += '),('
            newdatasets = newdatasets[:-2] + ';'
            insertsuccess = db.insertTable(pool, "department(departid,departname,departhead,telephone)", newdatasets)
            if insertsuccess == True:
                return render_template('department.html', inserterror="False")
            else:
                return render_template('department.html', inserterror="True")
        elif request.form.get('posttype') == 'modify':
            numj = request.form.get('numj')
            k = 0
            notmoddepartid = []
            moddepartid = []
            moddepartname = []
            moddeparthead = []
            modtelephone = []
            for i in range(int(numj)):
                notmoddepartid.append(request.form.get('departid' + str(i)))
                moddepartid.append(request.form.get('moddepartid' + notmoddepartid[i]))
                moddepartname.append(request.form.get('moddepartname' + notmoddepartid[i]))
                moddeparthead.append(request.form.get('moddeparthead' + notmoddepartid[i]))
                modtelephone.append(request.form.get('modtelephone' + notmoddepartid[i]))
            for i in range(int(numj)):
                modeddata = ""
                modeddata += 'departid="' + moddepartid[i] + '"'
                modeddata += ',departname="' + moddepartname[i] + '"'
                modeddata += ',departhead="' + moddeparthead[i] + '"'
                modeddata += ',telephone="' + modtelephone[i] + '"'
                pjdr = 'departid="' + notmoddepartid[i] + '"'
                modiifysuccess = db.modifyTable(pool, "department", modeddata, pjdr)
                if modiifysuccess == True:
                    k += 1
            return render_template('department.html', modifysuccessednum=str(k),
                                   modifyunsuccessednum=str(int(numj) - k))
        elif request.form.get('posttype') == 'delete':
            numk = request.form.get('numk')
            l = 0
            strdeletedepartids = request.form.get('deletekeys')
            deletedepartids = strdeletedepartids.split(' ')
            for i in range(int(numk)):
                deletesuccess = db.deletekeys(pool, 'department', "departid", '"' + deletedepartids[i] + '"')
                if deletesuccess == True:
                    l += 1
            return render_template('department.html', deletesuccessednum=str(l),
                                   deleteunsuccessednum=str(int(numk) - l))

@app.route('/class', methods=['GET', 'POST'], endpoint='classes')
@auth
def classes():
    if request.method == 'GET':
        return render_template('class.html')
    else:
        if request.form.get('posttype') == 'insert':
            numi = request.form.get('numi')
            newclassid = []
            newclassname = []
            newdepartid = []
            newbegindate = []
            newmaster = []
            newmastertel = []
            newdatasets = "("
            for i in range(int(numi)):
                newclassid.append(request.form.get('newclassid' + str(i + 1)))
                newclassname.append(request.form.get('newclassname' + str(i + 1)))
                newdepartid.append(request.form.get('newdepartid' + str(i + 1)))
                newbegindate.append(request.form.get('newbegindate' + str(i + 1)))
                newmaster.append(request.form.get('newmaster' + str(i + 1)))
                newmastertel.append(request.form.get('newmastertel' + str(i + 1)))
            for i in range(int(numi)):
                newdatasets += '"' + newclassid[i] + '",'
                newdatasets += '"' + newclassname[i] + '",'
                newdatasets += '"' + newdepartid[i] + '",'
                newdatasets += '"' + newbegindate[i] + '",'
                newdatasets += '"' + newmaster[i] + '",'
                newdatasets += '"' + newmastertel[i] + '"'
                newdatasets += '),('
            newdatasets = newdatasets[:-2] + ';'
            insertsuccess = db.insertTable(pool, "class(classid,classname,departid,begindate,master,mastertel)",
                                           newdatasets)
            if insertsuccess == True:
                return render_template('class.html', inserterror="False")
            else:
                return render_template('class.html', inserterror="True")
        elif request.form.get('posttype') == 'modify':
            numj = request.form.get('numj')
            k = 0
            notmodclassid = []
            modclassid = []
            modclassname = []
            moddepartid = []
            modbegindate = []
            modmaster = []
            modmastertel = []
            for i in range(int(numj)):
                notmodclassid.append(request.form.get('classid' + str(i)))
                modclassid.append(request.form.get('modclassid' + notmodclassid[i]))
                modclassname.append(request.form.get('modclassname' + notmodclassid[i]))
                moddepartid.append(request.form.get('moddepartid' + notmodclassid[i]))
                modbegindate.append(request.form.get('modbegindate' + notmodclassid[i]))
                modmaster.append(request.form.get('modmaster' + notmodclassid[i]))
                modmastertel.append(request.form.get('modmastertel' + notmodclassid[i]))
            for i in range(int(numj)):
                modclassdata = ""
                modclassdata += 'classid="' + modclassid[i] + '"'
                modclassdata += ',classname="' + modclassname[i] + '"'
                modclassdata += ',departid="' + moddepartid[i] + '"'
                modclassdata += ',begindate="' + modbegindate[i] + '"'
                modclassdata += ',master="' + modmaster[i] + '"'
                modclassdata += ',mastertel="' + modmastertel[i] + '"'
                pjdr = 'classid="' + notmodclassid[i] + '"'
                modiifysuccess = db.modifyTable(pool, "class", modclassdata, pjdr)
                if modiifysuccess == True:
                    k += 1
            return render_template('class.html', modifysuccessednum=str(k),
                                   modifyunsuccessednum=str(int(numj) - k))
        elif request.form.get('posttype') == 'delete':
            numk = request.form.get('numk')
            l = 0
            strdeletedepartids = request.form.get('deletekeys')
            deleteclassids = strdeletedepartids.split(' ')
            for i in range(int(numk)):
                deletesuccess = db.deletekeys(pool, 'class', "classid", '"' + deleteclassids[i] + '"')
                if deletesuccess == True:
                    l += 1
            return render_template('class.html', deletesuccessednum=str(l),
                                   deleteunsuccessednum=str(int(numk) - l))

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
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.getTable(pool, 'department', ['departid', 'departname', 'departhead', 'telephone'], sortBy, order,
                        search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage}},
        cls=dateJsonEncoder)

@app.route('/classdata', methods=['GET'], endpoint='classdata')
@auth
def classdata():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.getTable(pool, 'class', ['classid', 'classname', 'departid', 'begindate', 'master', 'mastertel'], sortBy,
                        order, search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage, "sortBy": sortBy, "order": order}},
        cls=dateJsonEncoder)

@app.route('/studata', methods=['GET'], endpoint='studata')
@auth
def studata():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.getTable(pool, 'student', ['studentid', 'name', 'sex', 'classid', 'birthday', 'native'], sortBy, order,
                        search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage, "sortBy": sortBy, "order": order}},
        cls=dateJsonEncoder)

@app.route('/changedata', methods=['GET'], endpoint='changedata')
@auth
def changedata():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.getTable(pool, 'changes', ['cid', 'changess', 'recdate', 'studentid'], sortBy, order, search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage, "sortBy": sortBy, "order": order}},
        cls=dateJsonEncoder)

@app.route('/rewarddata', methods=['GET'], endpoint='rewarddata')
@auth
def rewarddata():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.getTable(pool, 'reward', ['rid', 'studentid', 'reward', 'recdate'], sortBy, order, search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage, "sortBy": sortBy, "order": order}},
        cls=dateJsonEncoder)

@app.route('/punishdata', methods=['GET'], endpoint='punishdata')
@auth
def punishdata():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.getTable(pool, 'punish', ['pid', 'studentid', 'punish', 'recdate'], sortBy, order, search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage, "sortBy": sortBy, "order": order}},
        cls=dateJsonEncoder)

if __name__ == '__main__':
    app.run()
