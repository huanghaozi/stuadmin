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
    if request.method == 'GET':
        return render_template('student.html')
    else:
        if request.form.get('posttype') == 'insert':
            numi = request.form.get('numi')
            newstudentid = []
            newname = []
            newsex = []
            newclassid = []
            newbirthday = []
            newnative = []
            newdatasets = "("
            for i in range(int(numi)):
                newstudentid.append(request.form.get('newstudentid' + str(i + 1)))
                newname.append(request.form.get('newname' + str(i + 1)))
                newsex.append(request.form.get('newsex' + str(i + 1)))
                newclassid.append(request.form.get('newclassid' + str(i + 1)))
                newbirthday.append(request.form.get('newbirthday' + str(i + 1)))
                newnative.append(request.form.get('newnative' + str(i + 1)))
            for i in range(int(numi)):
                newdatasets += '"' + newstudentid[i] + '",'
                newdatasets += '"' + newname[i] + '",'
                newdatasets += '"' + newsex[i] + '",'
                newdatasets += '"' + newclassid[i] + '",'
                newdatasets += '"' + newbirthday[i] + '",'
                newdatasets += '"' + newnative[i] + '"'
                newdatasets += '),('
            newdatasets = newdatasets[:-2] + ';'
            insertsuccess = db.insertTable(pool, "student(studentid,name,sex,classid,birthday,native)",
                                           newdatasets)
            if insertsuccess == True:
                return render_template('student.html', inserterror="False")
            else:
                return render_template('student.html', inserterror="True")
        elif request.form.get('posttype') == 'modify':
            numj = request.form.get('numj')
            k = 0
            notmodstudentid = []
            modstudentid = []
            modname = []
            modsex = []
            modclassid = []
            modbirthday = []
            modnative = []
            for i in range(int(numj)):
                notmodstudentid.append(request.form.get('studentid' + str(i)))
                mmm = 'modname' + notmodstudentid[i]
                modstudentid.append(request.form.get('modstudentid' + notmodstudentid[i]))
                modname.append(request.form.get(mmm))
                modsex.append(request.form.get('modsex' + notmodstudentid[i]))
                modclassid.append(request.form.get('modclassid' + notmodstudentid[i]))
                modbirthday.append(request.form.get('modbirthday' + notmodstudentid[i]))
                modnative.append(request.form.get('modnative' + notmodstudentid[i]))
            for i in range(int(numj)):
                modstudentdata = ""
                modstudentdata += 'studentid="' + modstudentid[i] + '"'
                modstudentdata += ',name="' + modname[i] + '"'
                modstudentdata += ',sex="' + modsex[i] + '"'
                modstudentdata += ',classid="' + modclassid[i] + '"'
                modstudentdata += ',birthday="' + modbirthday[i] + '"'
                modstudentdata += ',native="' + modnative[i] + '"'
                pjdr = 'studentid="' + notmodstudentid[i] + '"'
                modiifysuccess = db.modifyTable(pool, "student", modstudentdata, pjdr)
                if modiifysuccess == True:
                    k += 1
            return render_template('student.html', modifysuccessednum=str(k),
                                   modifyunsuccessednum=str(int(numj) - k))
        elif request.form.get('posttype') == 'delete':
            numk = request.form.get('numk')
            l = 0
            strdeletedepartids = request.form.get('deletekeys')
            deletestudentids = strdeletedepartids.split(' ')
            for i in range(int(numk)):
                deletesuccess = db.deletekeys(pool, 'student', "studentid", '"' + deletestudentids[i] + '"')
                if deletesuccess == True:
                    l += 1
            return render_template('student.html', deletesuccessednum=str(l),
                                   deleteunsuccessednum=str(int(numk) - l))


@app.route('/courses', methods=['GET', 'POST'], endpoint='courses')
@auth
def courses():
    if request.method == 'GET':
        return render_template('courses.html')
    else:
        if request.form.get('posttype') == 'insert':
            numi = request.form.get('numi')
            newcourseid = []
            newcoursename = []
            newbegindate = []
            newplace = []
            newtime = []
            newenddate = []
            newevameans = []
            newstudyscore = []
            newdepartid = []
            newteacher = []
            newother = []
            newdatasets = "("
            for i in range(int(numi)):
                newcourseid.append(request.form.get('newcourseid' + str(i + 1)))
                newcoursename.append(request.form.get('newcoursename' + str(i + 1)))
                newbegindate.append(request.form.get('newbegindate' + str(i + 1)))
                newplace.append(request.form.get('newplace' + str(i + 1)))
                newtime.append(request.form.get('newtime' + str(i + 1)))
                newenddate.append(request.form.get('newenddate' + str(i + 1)))
                newevameans.append(request.form.get('newevameans' + str(i + 1)))
                newstudyscore.append(request.form.get('newstudyscore' + str(i + 1)))
                newdepartid.append(request.form.get('newdepartid' + str(i + 1)))
                newteacher.append(request.form.get('newteacher' + str(i + 1)))
                newother.append(request.form.get('newother' + str(i + 1)))
            for i in range(int(numi)):
                newdatasets += '"' + newcourseid[i] + '",'
                newdatasets += '"' + newcoursename[i] + '",'
                newdatasets += '"' + newbegindate[i] + '",'
                newdatasets += '"' + newplace[i] + '",'
                newdatasets += '"' + newtime[i] + '",'
                newdatasets += '"' + newenddate[i] + '",'
                newdatasets += '"' + newevameans[i] + '",'
                newdatasets += '"' + newstudyscore[i] + '",'
                newdatasets += '"' + newdepartid[i] + '",'
                newdatasets += '"' + newteacher[i] + '",'
                newdatasets += '"' + newother[i] + '"'
                newdatasets += '),('
            newdatasets = newdatasets[:-2] + ';'
            insertsuccess = db.insertTable(pool,
                                           "courses(courseid, coursename, begindate, place, time, enddate, evameans, studyscore, departid, teacher, other)",
                                           newdatasets)
            if insertsuccess == True:
                return render_template('courses.html', inserterror="False")
            else:
                return render_template('courses.html', inserterror="True")
        elif request.form.get('posttype') == 'modify':
            numj = request.form.get('numj')
            k = 0
            notmodcourseid = []
            modcourseid = []
            modcoursename = []
            modbegindate = []
            modplace = []
            modtime = []
            modenddate = []
            modevameans = []
            modstudyscore = []
            moddepartid = []
            modteacher = []
            modother = []
            for i in range(int(numj)):
                notmodcourseid.append(request.form.get('courseid' + str(i)))
                modcourseid.append(request.form.get('modcourseid' + notmodcourseid[i]))
                modcoursename.append(request.form.get('modcoursename' + notmodcourseid[i]))
                modbegindate.append(request.form.get('modbegindate' + notmodcourseid[i]))
                modplace.append(request.form.get('modplace' + notmodcourseid[i]))
                modtime.append(request.form.get('modtime' + notmodcourseid[i]))
                modenddate.append(request.form.get('modenddate' + notmodcourseid[i]))
                modevameans.append(request.form.get('modevameans' + notmodcourseid[i]))
                modstudyscore.append(request.form.get('modstudyscore' + notmodcourseid[i]))
                moddepartid.append(request.form.get('moddepartid' + notmodcourseid[i]))
                modteacher.append(request.form.get('modteacher' + notmodcourseid[i]))
                modother.append(request.form.get('modother' + notmodcourseid[i]))
            for i in range(int(numj)):
                modcoursedata = ""
                modcoursedata += 'courseid="' + modcourseid[i] + '"'
                modcoursedata += ',coursename="' + modcoursename[i] + '"'
                modcoursedata += ',begindate="' + modbegindate[i] + '"'
                modcoursedata += ',place="' + modplace[i] + '"'
                modcoursedata += ',time="' + modtime[i] + '"'
                modcoursedata += ',enddate="' + modenddate[i] + '"'
                modcoursedata += ',evameans="' + modevameans[i] + '"'
                modcoursedata += ',studyscore="' + modstudyscore[i] + '"'
                modcoursedata += ',departid="' + moddepartid[i] + '"'
                modcoursedata += ',teacher="' + modteacher[i] + '"'
                modcoursedata += ',other="' + modother[i] + '"'
                pjdr = 'courseid="' + notmodcourseid[i] + '"'
                modiifysuccess = db.modifyTable(pool, "courses", modcoursedata, pjdr)
                if modiifysuccess == True:
                    k += 1
            return render_template('courses.html', modifysuccessednum=str(k),
                                   modifyunsuccessednum=str(int(numj) - k))
        elif request.form.get('posttype') == 'delete':
            numk = request.form.get('numk')
            l = 0
            strdeletedepartids = request.form.get('deletekeys')
            deletestudentids = strdeletedepartids.split(' ')
            for i in range(int(numk)):
                deletesuccess = db.deletekeys(pool, 'courses', "courseid", '"' + deletestudentids[i] + '"')
                if deletesuccess == True:
                    l += 1
            return render_template('courses.html', deletesuccessednum=str(l),
                                   deleteunsuccessednum=str(int(numk) - l))


@app.route('/search', methods=['GET', 'POST'], endpoint='search')
@auth
def search():
    return render_template('search.html')

@app.route('/change', methods=['GET', 'POST'], endpoint='change')
@auth
def change():
    if request.method == 'GET':
        return render_template('change.html')
    else:
        if request.form.get('posttype') == 'insert':
            numi = request.form.get('numi')
            newstudentid = []
            newchangetype = []
            newrecdate = []
            newdatasets = "("
            for i in range(int(numi)):
                newstudentid.append(request.form.get('newstudentid' + str(i + 1)))
                newchangetype.append(request.form.get('newchangetype' + str(i + 1)))
                newrecdate.append(request.form.get('newrecdate' + str(i + 1)))
            for i in range(int(numi)):
                newdatasets += '"' + newstudentid[i] + '",'
                newdatasets += '"' + newchangetype[i] + '",'
                newdatasets += '"' + newrecdate[i] + '"'
                newdatasets += '),('
            newdatasets = newdatasets[:-2] + ';'
            insertsuccess = db.insertTable(pool, "changes(studentid,changess,recdate)",
                                           newdatasets)
            if insertsuccess == True:
                return render_template('change.html', inserterror="False")
            else:
                return render_template('change.html', inserterror="True")
        elif request.form.get('posttype') == 'modify':
            numj = request.form.get('numj')
            k = 0
            cid = []
            modstudentid = []
            modchangetype = []
            modrecdate = []
            for i in range(int(numj)):
                cid.append(request.form.get('cid' + str(i)))
                modstudentid.append(request.form.get('modstudentid' + cid[i]))
                modchangetype.append(request.form.get('modchangetype' + cid[i]))
                modrecdate.append(request.form.get('modrecdate' + cid[i]))
            for i in range(int(numj)):
                modstudentdata = ""
                modstudentdata += 'studentid="' + modstudentid[i] + '"'
                modstudentdata += ',changess="' + modchangetype[i] + '"'
                modstudentdata += ',recdate="' + modrecdate[i] + '"'
                pjdr = 'cid="' + cid[i] + '"'
                modiifysuccess = db.modifyTable(pool, "changes", modstudentdata, pjdr)
                if modiifysuccess == True:
                    k += 1
            return render_template('change.html', modifysuccessednum=str(k),
                                   modifyunsuccessednum=str(int(numj) - k))
        elif request.form.get('posttype') == 'delete':
            numk = request.form.get('numk')
            l = 0
            strdeletedepartids = request.form.get('deletekeys')
            deletestudentids = strdeletedepartids.split(' ')
            for i in range(int(numk)):
                deletesuccess = db.deletekeys(pool, 'changes', "cid", '"' + deletestudentids[i] + '"')
                if deletesuccess == True:
                    l += 1
            return render_template('change.html', deletesuccessednum=str(l),
                                   deleteunsuccessednum=str(int(numk) - l))

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
    if request.method == 'GET':
        return render_template('reward.html')
    else:
        if request.form.get('posttype') == 'insert':
            numi = request.form.get('numi')
            newstudentid = []
            newrewardtype = []
            newrecdate = []
            newdatasets = "("
            for i in range(int(numi)):
                newstudentid.append(request.form.get('newstudentid' + str(i + 1)))
                newrewardtype.append(request.form.get('newrewardtype' + str(i + 1)))
                newrecdate.append(request.form.get('newrecdate' + str(i + 1)))
            for i in range(int(numi)):
                newdatasets += '"' + newstudentid[i] + '",'
                newdatasets += '"' + newrewardtype[i] + '",'
                newdatasets += '"' + newrecdate[i] + '"'
                newdatasets += '),('
            newdatasets = newdatasets[:-2] + ';'
            insertsuccess = db.insertTable(pool, "reward(studentid,reward,recdate)",
                                           newdatasets)
            if insertsuccess == True:
                return render_template('reward.html', inserterror="False")
            else:
                return render_template('reward.html', inserterror="True")
        elif request.form.get('posttype') == 'modify':
            numj = request.form.get('numj')
            k = 0
            rid = []
            modstudentid = []
            modrewardtype = []
            modrecdate = []
            for i in range(int(numj)):
                rid.append(request.form.get('rid' + str(i)))
                modstudentid.append(request.form.get('modstudentid' + rid[i]))
                modrewardtype.append(request.form.get('modrewardtype' + rid[i]))
                modrecdate.append(request.form.get('modrecdate' + rid[i]))
            for i in range(int(numj)):
                modstudentdata = ""
                modstudentdata += 'studentid="' + modstudentid[i] + '"'
                modstudentdata += ',reward="' + modrewardtype[i] + '"'
                modstudentdata += ',recdate="' + modrecdate[i] + '"'
                pjdr = 'rid="' + rid[i] + '"'
                modiifysuccess = db.modifyTable(pool, "reward", modstudentdata, pjdr)
                if modiifysuccess == True:
                    k += 1
            return render_template('reward.html', modifysuccessednum=str(k),
                                   modifyunsuccessednum=str(int(numj) - k))
        elif request.form.get('posttype') == 'delete':
            numk = request.form.get('numk')
            l = 0
            strdeletedepartids = request.form.get('deletekeys')
            deletestudentids = strdeletedepartids.split(' ')
            for i in range(int(numk)):
                deletesuccess = db.deletekeys(pool, 'reward', "rid", '"' + deletestudentids[i] + '"')
                if deletesuccess == True:
                    l += 1
            return render_template('reward.html', deletesuccessednum=str(l),
                                   deleteunsuccessednum=str(int(numk) - l))


@app.route('/punish', methods=['GET', 'POST'], endpoint='punish')
@auth
def punish():
    if request.method == 'GET':
        return render_template('punish.html')
    else:
        if request.form.get('posttype') == 'insert':
            numi = request.form.get('numi')
            newstudentid = []
            newpunishtype = []
            newrecdate = []
            newdatasets = "("
            for i in range(int(numi)):
                newstudentid.append(request.form.get('newstudentid' + str(i + 1)))
                newpunishtype.append(request.form.get('newpunishtype' + str(i + 1)))
                newrecdate.append(request.form.get('newrecdate' + str(i + 1)))
            for i in range(int(numi)):
                newdatasets += '"' + newstudentid[i] + '",'
                newdatasets += '"' + newpunishtype[i] + '",'
                newdatasets += '"' + newrecdate[i] + '"'
                newdatasets += '),('
            newdatasets = newdatasets[:-2] + ';'
            insertsuccess = db.insertTable(pool, "punish(studentid,punish,recdate)",
                                           newdatasets)
            if insertsuccess == True:
                return render_template('punish.html', inserterror="False")
            else:
                return render_template('punish.html', inserterror="True")
        elif request.form.get('posttype') == 'modify':
            numj = request.form.get('numj')
            k = 0
            pid = []
            modstudentid = []
            modpunishtype = []
            modrecdate = []
            for i in range(int(numj)):
                pid.append(request.form.get('pid' + str(i)))
                modstudentid.append(request.form.get('modstudentid' + pid[i]))
                modpunishtype.append(request.form.get('modpunishtype' + pid[i]))
                modrecdate.append(request.form.get('modrecdate' + pid[i]))
            for i in range(int(numj)):
                modstudentdata = ""
                modstudentdata += 'studentid="' + modstudentid[i] + '"'
                modstudentdata += ',punish="' + modpunishtype[i] + '"'
                modstudentdata += ',recdate="' + modrecdate[i] + '"'
                pjdr = 'pid="' + pid[i] + '"'
                modiifysuccess = db.modifyTable(pool, "punish", modstudentdata, pjdr)
                if modiifysuccess == True:
                    k += 1
            return render_template('punish.html', modifysuccessednum=str(k),
                                   modifyunsuccessednum=str(int(numj) - k))
        elif request.form.get('posttype') == 'delete':
            numk = request.form.get('numk')
            l = 0
            strdeletedepartids = request.form.get('deletekeys')
            deletestudentids = strdeletedepartids.split(' ')
            for i in range(int(numk)):
                deletesuccess = db.deletekeys(pool, 'punish', "pid", '"' + deletestudentids[i] + '"')
                if deletesuccess == True:
                    l += 1
            return render_template('punish.html', deletesuccessednum=str(l),
                                   deleteunsuccessednum=str(int(numk) - l))


@app.route('/cladepa', methods=['GET'], endpoint='cladepa')
@auth
def cladepa():
    datas = db.getTable(pool, 'department', ['departid', 'departname', 'departhead', 'telephone'])
    noparsejson = {"departid": []}
    for i in range(len(datas)):
        noparsejson["departid"].append(datas[i]["departid"])
    jsonstr = json.dumps(noparsejson)
    return jsonstr


@app.route('/stucla', methods=['GET'], endpoint='stucla')
@auth
def stucla():
    datas = db.getTable(pool, 'class', ['classid', 'classname', 'departid', 'begindate', 'master', 'mastertel'])
    noparsejson = {"classid": []}
    for i in range(len(datas)):
        noparsejson["classid"].append(datas[i]["classid"])
    jsonstr = json.dumps(noparsejson)
    return jsonstr


@app.route('/stu', methods=['GET'], endpoint='stu')
@auth
def stu():
    datas = db.getTable(pool, 'student', ['studentid', 'name', 'sex', 'classid', 'birthday', 'native'])
    noparsejson = {"studentid": []}
    for i in range(len(datas)):
        noparsejson["studentid"].append(datas[i]["studentid"])
    jsonstr = json.dumps(noparsejson)
    return jsonstr


@app.route('/stuinfor', methods=['GET'], endpoint='stuinfor')
@auth
def stuinfor():
    searchxthc = request.args.get('searchxthc').split(' ')
    searchxkmk = request.args.get('searchxkmk').split(' ')
    datas = db.getTable(pool, 'student', ['studentid', 'name', 'sex', 'classid', 'birthday', 'native'])
    notinsearch = []
    if searchxkmk[0] != '' and searchxthc[0] != '':
        for xthcs in searchxthc:
            for xkmks in searchxkmk:
                for i in range(len(datas)):
                    if datas[i]["studentid"].find(xthcs) == -1 and datas[i]["name"].find(xkmks) == -1:
                        notinsearch.append(datas[i])
    elif searchxthc[0] != '' and searchxkmk[0] == '':
        for xthcs in searchxthc:
            for i in range(len(datas)):
                if datas[i]["studentid"].find(xthcs) == -1:
                    notinsearch.append(datas[i])
    elif searchxthc[0] == '' and searchxkmk[0] != '':
        for xkmks in searchxkmk:
            for i in range(len(datas)):
                if datas[i]["name"].find(xkmks) == -1:
                    notinsearch.append(datas[i])
    datas = db.listDifference(datas, notinsearch)
    jsonstr = json.dumps(datas, cls=dateJsonEncoder)
    return jsonstr

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
    for i in range(len(datas)):
        datas[i]["studentname"] = datas[i].pop("name")
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


@app.route('/coursesdata', methods=['GET'], endpoint='coursesdata')
@auth
def coursesdata():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.getTable(pool, 'courses',
                        ['courseid', 'coursename', 'begindate', 'place', 'time', 'enddate', 'evameans', 'studyscore',
                         'departid', 'teacher', 'other'], sortBy, order, search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage, "sortBy": sortBy, "order": order}},
        cls=dateJsonEncoder)


@app.route('/changedatainsearch', methods=['GET'], endpoint='changedatainsearch')
@auth
def changedatainsearch():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.searchTable(pool, 'changes', ['cid', 'changess', 'recdate', 'studentid'], sortBy, order, search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage, "sortBy": sortBy, "order": order}},
        cls=dateJsonEncoder)


@app.route('/punishdatainsearch', methods=['GET'], endpoint='punishdatainsearch')
@auth
def punishdatainsearch():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.searchTable(pool, 'punish', ['pid', 'studentid', 'punish', 'recdate'], sortBy, order, search)
    page = int(request.args.get('page'))
    recPerPage = int(request.args.get('recPerPage'))
    recTotal = len(datas)
    return json.dumps(
        {"result": "success", "data": datas[(page - 1) * recPerPage:page * recPerPage], "message": "未知错误",
         "pager": {"page": page, "recTotal": recTotal, "recPerPage": recPerPage, "sortBy": sortBy, "order": order}},
        cls=dateJsonEncoder)


@app.route('/rewarddatainsearch', methods=['GET'], endpoint='rewarddatainsearch')
@auth
def rewarddatainsearch():
    sortBy = request.args.get('sortBy')
    order = request.args.get('order')
    search = request.args.get('search')
    datas = db.searchTable(pool, 'reward', ['rid', 'studentid', 'reward', 'recdate'], sortBy, order, search)
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
