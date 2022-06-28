import re
import webbrowser
import json
import logging
import logging.config
import datetime
import pymssql
from flask import (Flask, Response, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure, OperationFailure

from flask_session import Session
import __init__ as appcfg


_MONTHTHAI = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
              'กรกฎาคม',  'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
app = Flask(__name__)
app.secret_key = 'secret'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MONGO_URI"] = "mongodb://192.168.1.230:27017/addrocrtha"
mongo = PyMongo(app)  # addrocrtha.personscan4
conllection = mongo.db.civil_registration
Session(app)
fileperpage = 10
ocrs = []
ocrlot = None
info = dict()

#
flog = './civil_regis.log'
logging.basicConfig(filename=flog, filemode='w',
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)
logging.info('Start app '+appcfg.__title__+' V'+appcfg.__version_short__)
app_ver = appcfg.__version_short__


def createdir(p):
    # เตรียมโฟรเดอร์เก็บไฟล์
    try:
        p.mkdir(parents=True)
    except FileExistsError as exc:
        print('Folder ' + p._str + '..........Ok ')


@app.route('/', methods=["POST", "GET"])
def index():
    if not session.get("name"):
        return redirect("/login")

    if session["sessionpage"] == 'sms':
        info = {'app': 'SDC',
                'logo': "http://192.168.1.241:3000/RecoveryScan/pic/Logo-CLT.png", "version": app_ver}
        return render_template("sms2.html", info=info, jsonmsg=None)
    elif session["sessionpage"] == 'civil':
        info = {'app': 'CDC',
                'logo': "http://192.168.1.241:3000/RecoveryScan/pic/Logo-CLT.png", "version": app_ver}
        return render_template("civil.html", info=info)

    info = {'app': 'PFD',
            'logo': "http://192.168.1.241:3000/RecoveryScan/pic/Logo-CLT.png", "version": app_ver}
    return render_template("index.html", info=info)


@app.route('/profile')
def profile():
    if not session.get("name"):
        return redirect("/login")

    session["sessionpage"] = None
    return render_template("index.html", info=info)


@app.route("/login", methods=["POST", "GET"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    version = '1.1.0'
    info = {'logo': "http://192.168.1.241:3000/RecoveryScan/pic/Logo-CLT.png",
            "version": app_ver}

    if request.method == "POST":
        # global conn, cursor
        conn = pymssql.connect('192.168.1.254', 'sa', 'mymasterdb', "address")
        cursor = conn.cursor()

        sql = "SELECT Pass,[user_name],name_sur,Picture,user_code,BroadCast1,Telno,mobileno,department,[Description],[db_name],[dept_view] FROM  EDOCUMENT.dbo.USER_PASS where user_name = %s AND Pass = %s AND inactive_user =0 "
        val = (username, password)
        cursor.execute(sql, val)
        row = cursor.fetchone()
        if row:
            session["user_name"] = username  # request.form.get("name")
            session["name"] = username  # request.form.get("name")
            r = dict((cursor.description[i][0], value)
                     for i, value in enumerate(row))
            session.update(r)
            session['Picture'] = str(session['Picture']).replace(
                "\\\\192.168.1.3\\loglawyer$\\pic\\", "http://192.168.1.241:3000/RecoveryScan/pic/").replace("\\", "/")
            session["remote_addr"] = request.remote_addr
            session["user_agent"] = [request.user_agent.platform, request.user_agent.browser,
                                     request.user_agent.version, request.user_agent.language]
            session["ocrlot"] = None
            session["sessionpage"] = None
            session['picture'] = session['Picture']
            session["info"] = dict()

            # 'Processs  Logging  Start'
            logging.info('User '+session["name_sur"]+' login success')
            logging.info(session["user_agent"])

            session["sessionpage"] = None
            conn.close()
            return redirect("/")
        else:
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', category='danger')
            return render_template("login.html", info=info, error="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render_template("login.html", info=info, error="")


@app.route("/sms2")
def sms2():
    if not session.get("name"):
        return redirect("/login")
    else:
        data = {'app': 'SDC'}
        data['user_code'] = session['user_code']
        data['db_name'] = session['db_name']
        data['dept_view'] = session['dept_view']
        import requests  # IP:5001/get_phonebooks_by_user
        url = 'http://192.168.1.28:5001/get_phonebooks_by_user'
        res = requests.post(url, json=data)
        if res.status_code == 200:
            result = res.json()
            if 'Error' in result['msg']:
                print(result['msg'])
                session["phonebooks"] = None
                session["smsbox"] = None
            else:
                session["phonebooks"] = None if result['phonebooks'] == [
                ] else result['phonebooks']
                session["smsbox"] = None if result['smsbox'] == [
                ] else result['smsbox']
            session["sessionpage"] = 'sms'
            session["smsboxcount"] = len(session["smsbox"])
            session["smsbox"] = formatdate_easy(session["smsbox"])
            return redirect("/")
        else:
            return redirect("/login")


def formatdate_easy(smsbox):
    f3 = '%a, %d %b  %Y %H:%M:%S GMT'
    of1 = '%a %d-%m-%Y %H:%M:%S'
    for i in range(len(smsbox)):
        if smsbox[i].get('cdrcall') is not None:
            date_time_obj = datetime.datetime.strptime(
                smsbox[i]['cdrcall'], f3)
            if datetime.datetime.now().date() == date_time_obj.date():
                smsbox[i]['cdrcall'] = str(
                    date_time_obj.strftime('%H:%M:%S'))
            else:
                smsbox[i]['cdrcall'] = str(date_time_obj.strftime(of1))

        if len(smsbox[i]['timestamp']) >= 19:
            date_time_obj = datetime.datetime.strptime(
                smsbox[i]['timestamp'], f3)
            if datetime.datetime.now().date() == date_time_obj.date():
                smsbox[i]['timestamp'] = str(
                    date_time_obj.strftime('%H:%M:%S'))
            else:
                smsbox[i]['timestamp'] = str(date_time_obj.strftime(of1))
        else:
            smsbox[i]['timestamp'] = smsbox[i]['timestamp']
        if smsbox[i]['company_code'] is None:
            smsbox[i]['company_code'] = ''
        if smsbox[i]['account_name'] is None:
            smsbox[i]['account_name'] = ''
        if smsbox[i]['account_no'] is None:
            smsbox[i]['account_no'] = ''

    return smsbox


@app.route("/sendsms", methods=['POST'])
def sendsms():
    dumdict = request.form.to_dict()
    sms = dict()
    sms['number'] = dumdict['number']
    sms['text'] = session['BroadCast1']
    import requests
    url = 'http://192.168.1.28:5002/sendsms'
    res = requests.post(url,  json=sms)
    result = res.json()
    print(result)
    result['text'] = session['BroadCast1']
    result['user'] = session['user_code']
    session["sessionpage"] = 'sms'
    if result['status'] == 'DELIVERED':
        conn = pymssql.connect('192.168.1.254', 'sa',
                               'mymasterdb', "EDOCUMENT")
        cursor = conn.cursor()

        sql = "UPDATE EDOCUMENT.dbo.phonebooks SET  sms_user = %s ,sms =%s , sms_timestmp = getdate() Where tel_no = %s "
        val = (session['user_code'], session['BroadCast1']
               [:200], dumdict['number'])
        try:
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)
            conn.rollback()
            cursor.close()
            conn.close()

    return json.dumps(result)


@app.route('/toggleUpdate', methods=['POST'])
def toggleUpdate():
    if not session.get("name"):
        return redirect("/login")

    dumdict = request.form.to_dict()
    myquery = {'index_of_lotfile': int(
        dumdict['index_of_lotfile']), 'ocrlot': session["ocrlot"]}
    # print(' index_of_lotfile ', str(    #     dumdict['index_of_lotfile']), ' Check =', str(dumdict['checked']))
    dumdict = dict(request.form)
    if dumdict['checked'] == '1':
        conllection.update_one(myquery, {'$set': {'checked': 0}})
        print(session['name'], session["ocrlot"], 'index_of_lotfile', str(
            dumdict['index_of_lotfile']), '=====> Unchecked')
        logging.info('%s %s %s %s %s', session['name'], session["ocrlot"], 'index_of_lotfile', str(
            dumdict['index_of_lotfile']), '=====> Unchecked')

        return json.dumps('Cancle')

    dumdict['checked'] = 1
    # print(session['name'], session["ocrlot"], 'index_of_lotfile', str(
    #     dumdict['index_of_lotfile']), '=====> Checked')
    logging.info('%s %s %s %s %s', session['name'], session["ocrlot"], 'index_of_lotfile', str(
        dumdict['index_of_lotfile']), '=====> Checked')

    # conllection.update_one(myquery, {'$set': {'checked': 1}})
    # return json.dumps('Checked')
    dumdict.pop('index_of_lotfile')
    newvalues = {"$set": dumdict}
    conllection.update_one(myquery, newvalues)
    return json.dumps('Update')


@app.route("/logout")
def logout():
    logging.info('User '+session["name"]+' Logout ')
    session.clear()
    return redirect("/")


@app.route('/civil')
def civil():

    if not session.get("name"):
        return redirect("/login")
    else:
        #  FIND  LAST session["ocrlot"]  TO FIND session["ocrlot"] DISPLAY
        #  DEBUG TEST  56
        conllection = mongo.db.civil_registration
        if session["ocrlot"] == None:
            session["ocrlot"] = mongo.db.counters.find_one({'_id': 'lotocr'})[
                'seq_value']
            ocrs = (list(conllection.aggregate([{'$group': {
                '_id': "$ocrlot",
                'ocrdocs': {'$sum': 1}
            }},
                {'$sort': {'_id': -1}}, {"$limit": 5}])))
        else:
            ocrs = (list(conllection.aggregate([{'$group': {
                '_id': "$ocrlot",
                'ocrdocs': {'$sum': 1}
            }},
                {'$sort': {'_id': -1}}, {"$limit": 5}])))

        totalcheked = conllection.count_documents(
            {"ocrlot": session["ocrlot"], "checked": 1})
        totalfile = conllection.count_documents({"ocrlot": session["ocrlot"]})
        listpage = (totalfile//fileperpage)
        if totalfile % fileperpage > 0:
            listpage += 1
        page = 0
        logging.info('Server session["ocrlot"] =>' +
                     session["name"] + ' ' + str(session["ocrlot"]))

        session["info"]["ocrs"] = ocrs
        session["info"]["ocrdata"] = []

        session["page"] = page
        session["listpage"] = listpage
        session["totalcheked"] = totalcheked
        session["totalfile"] = totalfile
        session["sessionpage"] = 'civil'
        info = {'app': 'CDC', "version": app_ver}
        return render_template('civil.html',  ocrdata=[], info=info)


@app.route('/setocr/<int:setocr>')
def setocr(setocr):
    # global info
    # global ocrlot
    if not session.get("name"):
        return redirect("/login")

    # chkocrlot = 0
    conllection = mongo.db.civil_registration
    session["ocrlot"] = int(setocr)

    totalcheked = conllection.count_documents(
        {"ocrlot": session["ocrlot"], "checked": 1})
    totalfile = conllection.count_documents({"ocrlot": session["ocrlot"]})
    listpage = (totalfile//fileperpage)
    if totalfile % fileperpage > 0:
        listpage += 1
    page = 0
    # print(session["name"], ' Change ocrlot ==> ', session["ocrlot"])
    logging.info('User '+session["name_sur"]+' Change ocrlot ==> '+str(
        session["ocrlot"])+' page '+str(page)+' listpage '+str(listpage)+' totalcheked '+str(totalcheked)+' totalfile '+str(totalfile))

    session["page"] = page
    session["listpage"] = listpage
    session["totalcheked"] = totalcheked
    session["totalfile"] = totalfile

    # info = {}
    info = {'app': 'CDC', "version": app_ver}
    return render_template('civil.html',  ocrdata=[], info=info)


def fnc_thatocmsdate(str_date=None):
    if str_date is None:
        return "NULL"
    else:
        if len(str_date.split()) == 3:
            d = str_date.split()[0] if int(str_date.split()[0]) < 31 else '1'
            m = str_date.split()[1]  # if str_date.split()[1].isalpha() else 1
            y = int(str_date.split()[2])-543
        elif len(str_date.split()) == 2:
            d = 1
            m = str_date.split()[0] if str_date.split()[0].isalpha() else 1
            y = int(str_date.split()[1])-543
            return "'" + str(y)+str(m).zfill(2)+str(d).zfill(2) + "'"

        elif len(str_date.split()) == 1:
            d = 1
            m = 1
            y = int(str_date.split()[0])-543
            return "'" + str(y)+str(m).zfill(2)+str(d).zfill(2) + "'"

    return "'" + str(y)+str(_MONTHTHAI.index(m)+1).zfill(2)+str(d).zfill(2) + "'"


def finddocumentcmissthai(stldata):
    try:
        x = mongo.db.cmissthai.find_one(stldata)
        return x
    except OperationFailure as e:
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}")
    return
#  INSERT ONE STLDATA DICT FORMAT


def get_zipcode(doc):
    finddict = dict()
    finddict['PROVINCE'] = doc['PROVINCE']
    finddict['TUMBUL'] = doc['TUMBUL']
    finddict['AUMPUR'] = doc['AUMPUR']
    # PROVINCE:"กระบี่"AUMPUR:"เกาะลันตา"TUMBUL:"เกาะกลาง"ZIPCODE:81120addrocrtha.loctha
    try:
        x = mongo.db.loctha.find_one(finddict)
        return x['ZIPCODE']
    except OperationFailure as e:
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}")
    return None


def Insertmissword(stldata):
    import datetime
    try:
        x = mongo.db.cmissthai.insert_one(stldata)
        return x
    except OperationFailure as e:
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}")
    return


@app.route('/findtel_no', methods=['POST', 'GET'])  #
def findtel_no():
    # global info
    if not session.get("name"):
        return redirect("/login")
    if request.method == 'POST':
        dumdict = request.form.to_dict()
        if "-" in dumdict['tel_nof']:
            dumdict['tel_nof'] = dumdict['tel_nof'].replace("-", "")
        if " " in dumdict['tel_nof']:
            dumdict['tel_nof'] = dumdict['tel_nof'].replace(" ", "")
        if len(dumdict['tel_nof']) != 10:
            flash('หมายเลขเบอร์ไม่ถูกต้อง', category='danger')
            return redirect("/sms2")
        else:
            #  FIND  DATA TO DICT FOR  DISPLAY idcard:"3-7302-00939-64-3"
            # /get_phonebook_info/<str: number >
            import requests
            url = 'http://192.168.1.28:5001/get_phonebook_info/' + \
                dumdict['tel_nof']
            res = requests.get(url)
            if res.status_code == 200:
                result = res.json()

                session["phone_info"] = result['phone_info'][0] if len(
                    result['phone_info']) > 0 else None
                session["smsbox"] = result['smsbox']
                session["smsboxcount"] = len(session["smsbox"])

                session["sessionpage"] = 'sms'
                info = {'app': 'SDC',
                        'logo': "http://192.168.1.241:3000/RecoveryScan/pic/Logo-CLT.png", "version": app_ver}

                return render_template('mobile.html',  info=info)
            else:
                flash('ไม่พบหมายเลขเบอร์', category='danger')
                return redirect("/sms2")
    else:
        return redirect("/sms2")


@app.route('/findidcard', methods=['POST', 'GET'])  #
def findidcard():
    # global info
    if not session.get("name"):
        return redirect("/login")
    # idc = request.form.items["search"]
    dumdict = request.form.to_dict()
    if "-" in dumdict['idcard']:
        dumdict['idcard'] = dumdict['idcard'].replace("-", "")
    if " " in dumdict['idcard']:
        dumdict['idcard'] = dumdict['idcard'].replace(" ", "")
    if len(dumdict['idcard']) == 13:
        #  FIND  DATA TO DICT FOR  DISPLAY idcard:"3-7302-00939-64-3"
        dumdict['idcard'] = dumdict['idcard'][0:1]+"-" + \
            dumdict['idcard'][1:5]+"-"+dumdict['idcard'][5:10]+"-" + \
            dumdict['idcard'][10:12]+"-"+dumdict['idcard'][12:13]
        ocrdata = conllection.find(dumdict)
        if ocrdata.count() > 0:
            stridcard = str(dumdict['idcard'])
            return json.dumps(stridcard)
            # return redirect(url_for('idcard', idcard=stridcard))
        else:
            return json.dumps('notfound')
        # return render_template('finddata.html', ocrdata=ocrdata, page=int(0),  info=info)
    else:
        return json.dumps('notfound')


@app.route('/idcard/<idcard>')
def idcard(idcard):
    global info
    if not session.get("name"):
        return redirect("/login")

    idcard = json.loads(idcard)
    ocrdata = conllection.find({'idcard': idcard})
    return render_template('finddata.html', ocrdata=ocrdata, info=info)


@app.route('/page/<int:page>')
def page(page):
    if not session.get("name"):
        return redirect("/login")

    global info

    """Update a author."""
    skipfile = fileperpage*int(page)
    totalcheked = conllection.count_documents(
        {"ocrlot": session["ocrlot"], "checked": 1})
    session["page"] = page

    ocrdata = conllection.find({"ocrlot": session["ocrlot"]}).limit(
        fileperpage).skip(skipfile).sort("index_of_lotfile", 1)

    session["page"] = page
    session["totalcheked"] = totalcheked

    logging.info('%s %s %s %s %s ', session["name"], 'session["ocrlot"] =>',
                 session["ocrlot"], 'page =>', page)

    return render_template('civil.html', ocrdata=ocrdata, page=int(page),  info=info, audit=session["name"])
    #    listpage=listpage,totalcheked=totalcheked,totalfile=totalfile)


@ app.route('/mongo2sql', methods=['POST', 'GET'])
def mongo2sql():
    info = {'app': 'SDC',
            'logo': "http://192.168.1.241:3000/RecoveryScan/pic/Logo-CLT.png", "version": app_ver}
    if not session.get("name"):
        return redirect("/login")
    if session["name"] != "wasan":
        flash("คุณไม่มีสิทธิ์ในการเข้าถึงหน้านี้", category='danger')
        return redirect("/")
    if request.method == "POST":
        import requests
        if request.form['act'] == "transfer":
            flash('กำลังนำข้อมูลไปยังฐานข้อมูล', category='success')
            # webbrowser.open_new(
            #     f'http://192.168.1.28:5001/mongo2sql/' + str(session["ocrlot"]))
            return redirect("/mongo2sql")
        elif request.form['act'] == "smsservice":
            r = requests.get('http://192.168.1.28:5001/service/sms')
            jsonmsg = r.json()
            flash(((str(jsonmsg))), category='success')
            return redirect("/mongo2sql")
        elif request.form['act'] == "fileocr":
            r = requests.get('http://192.168.1.28:5001/fileocr')
            jsonmsg = r.json()
            flash(((str(jsonmsg))), category='success')
            return redirect("/mongo2sql")
        elif request.form['act'] == "pyocr":
            # webbrowser.open_new(f'http://192.168.1.28:5001/pyocr')
            flash("กำลังทำการอ่านรูปภาพ", category='success')
            return redirect("/mongo2sql")
        elif request.form['act'] == "transferservice":
            r = requests.get('http://192.168.1.28:5001/service/transfer')
            jsonmsg = r.json()
            flash(((str(jsonmsg))), category='success')
            return redirect("/mongo2sql")
        elif request.form['act'] == "scanservice":
            r = requests.get('http://192.168.1.28:5001/service/scan')
            jsonmsg = r.json()
            flash(((str(jsonmsg))), category='success')
            return redirect("/mongo2sql")
        elif request.form['act'] == "apiservice":
            r = requests.get('http://192.168.1.28:5001/service/api')
            jsonmsg = r.json()
            flash(((str(jsonmsg))), category='success')
            return redirect("/mongo2sql")

        elif request.form['act'] == "mailservice":
            r = requests.get('http://192.168.1.28:5002')
            jsonmsg = r.json()
            flash(((str(jsonmsg))), category='success')
            return redirect("/mongo2sql")
        elif request.form['act'] == "addcmis":
            if "" == request.form['misword'] or "" == request.form['rghword']:
                flash('กรุณากรอกข้อมูลให้ครบ', category='danger')
                return redirect("/mongo2sql")
            if finddocumentcmissthai({'misword': request.form['misword']}) == None:
                dumdict = request.form.to_dict()
                dumdict['fcount'] = 1
                x = Insertmissword(dumdict)
                flash('บันทึกคำเรียบร้อย', category='success')
                return redirect("/mongo2sql")

        elif request.form['act'] == "chgocrlot":
            session["ocrlot"] = int(request.form['ocrlot'])
            flash('เปลี่ยนเป็น Lot :' +
                  str(session["ocrlot"]), category='success')
    conllection = mongo.db.civil_registration
    myquery = {'ocrlot': session["ocrlot"], 'checked': 1}
    totalcheked = conllection.count_documents(myquery)

    myquery = {'ocrlot': session["ocrlot"], 'loaddate': {
        "$exists": True, "$ne": None}}
    totalloaddate = conllection.count_documents(myquery)

    myquery = {'ocrlot': session["ocrlot"], 'loaddate': None}
    totalunloaddate = conllection.count_documents(myquery)
    session['transfer'] = "ข้อมูลทั้งหมด :" + str(totalcheked) + " รายการ"
    session['loaddata'] = "Load data: " + \
        str(totalloaddate) + " / " + str(totalunloaddate) + " รายการ"
    session['totalunloaddate'] = totalunloaddate

    return render_template('mongo2sql.html', info=info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=3000)

    # @app.route('/progress')
    # def progress():
    #     def generate():
    #         x = 0
    #         while x <= 100:
    #             yield "data:" + str(x) + "nn"
    #             x = x + 10
    #             time.sleep(0.5)=
    #     return Response(generate(), mimetype="text/event-stream")

    # @ app.route('/transfer')
# def transfer():
#     if not session.get("name"):
#         return redirect("/login")

#     global conn
#     global cursor
#     conn = pymssql.connect('192.168.1.254', 'sa', 'mymasterdb', "address")
#     cursor = conn.cursor()  # as_dict=True

#     conllection = mongo.db.civil_registration
#     myquery = {'ocrlot': session["ocrlot"], 'checked': 1}
#     totalcheked = conllection.count_documents(myquery)

#     myquery = {'ocrlot': session["ocrlot"], 'loaddate': {
#         "$exists": True, "$ne": None}}
#     totalloaddate = conllection.count_documents(myquery)

#     myquery = {'ocrlot': session["ocrlot"], 'loaddate': None}
#     totalunloaddate = conllection.count_documents(myquery)
#     session['transfer'] = "ข้อมูลทั้งหมด :" + str(totalcheked) + " รายการ"
#     session['loaddata'] = "Load data: " + \
#         str(totalloaddate) + " / " + str(totalunloaddate) + " รายการ"
#     session['totalunloaddate'] = totalunloaddate
#     return render_template('mongo2sql.html')

#     # info['transfer'] = ' transfer' + \
#     #     str(scount) + ' รายการ'+' จาก '+str(ccount) + ' รายการ'
#     # return render_template('transfer.html', info=info)


# UPS: Started a Daily scheduled switched outlet group shutdown 'Daily Shutdown'.

# wasan.k@chalinthon.co.th

# Name: UPS1000SMT
# Location: 98/28 2nd Bangkok
# Contact: IT MANAGER

# http: // apc1AB2A8.chalinthon.local
# http: // 192.168.1.250

# http: // [FE80::2A29:86FF:FE1A:B2A8](Local)
# http: // []

# Serial Number: ZA1914003161
# Device Serial Number: AS1930263841
# Date: 06/15/2022
# Time: 22: 00: 00
# Code: 0x017C

# Informational - UPS: Started a Daily scheduled switched outlet group shutdown 'Daily Shutdown'.
    # session["name"] = row[1]
    # session["name_sur"] = row[2]
    # session["user_code"] = row[4]
    # session["BroadCast1"] = row[5]
    # session["Telno"] = row[6]
    # session["mobileno"] = row[7]
    # session["department"] = row[8]
    # session["Description"] = row[9]
    # session["db_name"] = row[10]
    # http://192.168.1.241:3000/RecoveryScan/pic/1/login.gif   '\\\\192.168.1.3\\loglawyer$\\pic\\WASAN\\login.gif'
    # sql = '''
    # SELECT  pb.Account_no , '' as OpenAc , '' as user_code , pb.account_name, pb.company_code
    # , s.[number] as 'tel_no' , s.[timestamp], s.[text]
    # FROM EDOCUMENT.dbo.smsbox s LEFT OUTER JOIN EDOCUMENT.dbo.phonebooks pb ON s.number = pb.tel_no
    # where pb.tel_no is null and s.number like '0%' and (LEN(s.[text])=71 or LEN(s.[text]) < 50)
    # AND convert(varchar(8),s.timestmp ,112) =convert(varchar(8),getdate(),112)
    # ORDER BY s.[timestamp] desc
    # '''

# @app.route("/sendmail", methods=['GET', 'POST'])
# def sendmail():
#     if not session.get("name"):
#         return redirect("/login")
#     if request.method == "POST":
#         dumdict = dict(request.form)

#         msg = Message('FLASK Mail', sender='it.support@chalinthon.co.th',
#                       recipients=[dumdict['email']])
#         msg.body = dumdict['textmsg']
#         mail.send(msg)
#         flash('Mail sent')

#     return redirect("/")
# app.config['MAIL_SERVER'] = 'mail.chalinthon.co.th'
# app.config['MAIL_PORT'] = 25
# app.config['MAIL_USERNAME'] = 'it.support@chalinthon.co.th'
# app.config['MAIL_PASSWORD'] = 'Abc123456!'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = False
# mail = Mail(app)
# import webbrowser
# import datetime
# from datetime import date
# from pathlib import Path
# from webbrowser import get

# @app.route('/addmissword', methods=['POST'])
# def addmissword():
#     if not session.get("name"):
#         return redirect("/login")

#     dumdict = request.form.to_dict()
#     if "" == dumdict['misword'] or "" == dumdict['rghword']:
#         flash('กรุณากรอกข้อมูลให้ครบ', category='danger')
#         return redirect("/mongo2sql")
#     # has IDCARD change to Append & Update
#     if finddocumentcmissthai({'misword': dumdict['misword']}) == None:
#         dumdict['fcount'] = 1
#         x = Insertmissword(dumdict)
#     return json.dumps('add')

# @app.route("/service_sms")
# def service_sms():
#     if not session.get("name"):
#         return redirect("/login")
#     else:
#         import requests
#         r = requests.get('http://192.168.1.28:5002')
#         jsonmsg = r.json()
#         session["sessionpage"] = 'sms'
#     info = {'app': 'SDC',
#             'logo': "http://192.168.1.241:3000/RecoveryScan/pic/Logo-CLT.png", "version": app_ver}
#     return render_template("sms2.html", info=info, jsonmsg=jsonmsg)

# @app.route('/searchidcard', methods=['POST'])  #
# def searchidcard():
#     global info
#     if not session.get("name"):
#         return redirect("/login")

#     idc = request.form["search"]

#     dumdict = request.form.to_dict()
#     if "-" in dumdict['idcard']:
#         dumdict['idcard'] = dumdict['idcard'].replace("-", "")
#     if " " in dumdict['idcard']:
#         dumdict['idcard'] = dumdict['idcard'].replace(" ", "")
#     if len(dumdict['idcard']) == 13:
#         #  FIND  DATA TO DICT FOR  DISPLAY idcard:"3-7302-00939-64-3"
#         dumdict['idcard'] = dumdict['idcard'][0:1]+"-" + \
#             dumdict['idcard'][1:5]+"-"+dumdict['idcard'][5:10]+"-" + \
#             dumdict['idcard'][10:12]+"-"+dumdict['idcard'][12:13]
#         ocrdata = conllection.find(dumdict)
#         if ocrdata.count() > 0:
#             stridcard = str(dumdict['idcard'])
#             # return redirect(url_for('idcard', idcard=stridcard))
#             return json.dumps(stridcard)
#         else:
#             return json.dumps('notfound')
#         # return render_template('finddata.html', ocrdata=ocrdata, page=int(0),  info=info)
#     else:
#         return json.dumps('wrongID')

# @app.route("/mobileinfo")
# def mobileinfo():
#     if not session.get("name"):
#         return redirect("/login")
#     else:
#         session["sessionpage"] = 'sms'
#         return redirect("/")

# @app.route("/sms")
# def sms():
#     if not session.get("name"):
#         return redirect("/login")
#     else:
#         logging.info('User '+session["name_sur"]+' SMS Center Online success')
#         # global conn, cursor
#         conn = pymssql.connect('192.168.1.254', 'sa',
#                                'mymasterdb', "EDOCUMENT")
#         cursor = conn.cursor()

#         if session["db_name"] == 'ALL':
#             session["phonebooks"] = []
#         else:
#             sql = '''
#                     select  ROW_NUMBER ()OVER (	ORDER BY ac.timestmp desc ) row_number
#                     , ac.Account_no
#                     , ac.timestmp as OpenAc
#                     , left(pb.account_name,30) as account_name
#                     , pb.company_code
#                     , pb.tel_no
#                     , pb.sms
#                     , pb.sms_user
#                     , pb.sms_timestmp
#                     , ac.LOGDESC as user_code
#                     FROM {{session["db_name"]}}ACC_OPEN ac Inner JOIN
#                     EDOCUMENT.dbo.phonebooks pb ON ac.Account_no = pb.account_no
#                     WHERE  ac.LOGDESC= {{session["user_code"]}}
#             '''
#             sql = sql.replace(
#                 '{{session["db_name"]}}', session["db_name"]+'.dbo.')
#             sql = sql.replace(
#                 '{{session["user_code"]}}', "'" + session["user_code"]+"'")
#             cursor.execute(sql)

#             r = [dict((cursor.description[i][0], value)
#                       for i, value in enumerate(row)) for row in cursor.fetchall()]
#             session["phonebooks"] = (r[0] if r else None) if len(r) == 0 else r
#             # print(session["phonebooks"])
#         sql = '''
#                 SELECT   ROW_NUMBER ()OVER (	ORDER BY s.[timestamp] desc ) row_number
#                     ,pb.Account_no  as account_no
#                 , pb.account_name
#                 , pb.company_code
#                 , s.[number]
#                 , s.[timestamp]
#                 , s.[text]
#                 FROM EDOCUMENT.dbo.smsbox s LEFT OUTER JOIN EDOCUMENT.dbo.phonebooks pb ON s.number = pb.tel_no
#                 WHERE  s.number like '0%'  AND s.[timestamp] > DATEADD(day,-10,GETDATE())
#                 AND (  pb.company_code in ({{session["dept_view"]}}) OR pb.company_code is null )
#              '''
#         #  and (LEN(s.[text])=71 or LEN(s.[text]) < 50)
#         sql = sql.replace('{{session["dept_view"]}}',
#                           "'"+session["dept_view"]+"'")
#         cursor.execute(sql)

#         s = [dict((cursor.description[i][0], value)
#                   for i, value in enumerate(row)) for row in cursor.fetchall()]
#         session["smsbox"] = (s[0] if s else None) if len(s) == 0 else s

#         # --AND convert(varchar(8),s.timestmp ,112) =convert(varchar(8),getdate(),112)
#         # print(session["smsbox"])
#         cursor.close()
#         conn.close()
#         # return render_template("sms.html", data=cursor)
#         session["sessionpage"] = 'sms'

#     return redirect("/")
