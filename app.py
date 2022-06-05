import datetime
import json
import logging
import logging.config
import os
from datetime import date
from gettext import find
from pathlib import Path
from webbrowser import get
# from twilio.rest import Client

import pymssql
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_pymongo import PyMongo
from pymongo.errors import ConnectionFailure, OperationFailure

from flask_session import Session

# logging.config.fileConfig('logging.conf')

# create logger
# logger = logging.getLogger('simpleExample')TWILIO_ACCOUNT_SID
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                     body="หนี้สินมีทางออก KK กดเพิ่มเพื่อนที่ Link https://lin.ee/D1O5JX4 ",
#                     from_='+19125518330',
#                     to='+66813581828'
#                 )

# print(message.sid)


_MONTHTHAI = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
              'กรกฎาคม',  'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
app = Flask(__name__)
app.secret_key = 'secret'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MONGO_URI"] = "mongodb://192.168.1.230:27017/addrocrtha"
mongo = PyMongo(app)  # addrocrtha.personscan4
Session(app)
# conllection = mongo.db.personscan5 civil_registration
conllection = mongo.db.civil_registration
fileperpage = 10
ocrs = []
ocrlot = None
info = dict()
version = 1.3
conn, cursor = None, None
# SESSION LOGIN

#  INSERT ONE STLDATA DICT FORMAT


@app.route('/')
def index():
    global info
    global ocrlot
    global ocrs

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

            # for index, os in enumerate(ocrs):
            #     print(os, index)
        totalcheked = conllection.count_documents(
            {"ocrlot": session["ocrlot"], "checked": 1})
        totalfile = conllection.count_documents({"ocrlot": session["ocrlot"]})
        listpage = (totalfile//fileperpage)
        if totalfile % fileperpage > 0:
            listpage += 1
        page = 0
        # print('Server session["ocrlot"] =>',
        #       session["name"], session["ocrlot"])
        logging.info('Server session["ocrlot"] =>' +
                     session["name"] + ' ' + str(session["ocrlot"]))

        session["page"] = page
        session["listpage"] = listpage
        session["totalcheked"] = totalcheked
        session["totalfile"] = totalfile

        info = {'totalcheked': totalcheked,  'conllection': 'civil_regis',
                'totalfile': totalfile, 'listpage': listpage, "ocrlot": session["ocrlot"], "version": version, "page": page, "ocrs": ocrs}
        return render_template('base.html',  ocrdata=[], listpage=listpage, info=info, totalcheked=totalcheked, totalfile=totalfile)


@app.route("/logout")
def logout():
    logging.info('User '+session["name_sur"]+' Logout success')
    session["name"] = None
    session["ocrlot"] = None
    return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    info = {'totalcheked': 0,  'conllection': 'civil_regis', 'logo': "http://192.168.1.241:3000/RecoveryScan/pic/Logo-CLT.png",
            'totalfile': 0, 'listpage': 0, "ocrlot": 0, "version": version, "page": 0}

    if request.method == "POST":
        global conn, cursor
        conn = pymssql.connect('192.168.1.254', 'sa', 'mymasterdb', "address")
        cursor = conn.cursor()

        sql = "SELECT Pass,user_name,name_sur,Picture FROM  EDOCUMENT.dbo.USER_PASS where user_name = %s AND Pass = %s "
        val = (username, password)
        cursor.execute(sql, val)
        row = cursor.fetchone()
        if row:
            session["name"] = row[1]
            session["name_sur"] = row[2]
            # http://192.168.1.241:3000/RecoveryScan/pic/1/login.gif   '\\\\192.168.1.3\\loglawyer$\\pic\\WASAN\\login.gif'
            session["picture"] = str(row[3]).replace(
                "\\\\192.168.1.3\\loglawyer$\\pic\\", "http://192.168.1.241:3000/RecoveryScan/pic/")
            session["picture"] = session["picture"].replace("\\", "/")
            session["name"] = username  # request.form.get("name")
            session["remote_addr"] = request.remote_addr

            session["user_agent"] = [request.user_agent.platform, request.user_agent.browser,
                                     request.user_agent.version, request.user_agent.language]
            session["ocrlot"] = None
            # print('User ', session["name_sur"], ' login success',
            #       session["remote_addr"], session["user_agent"])

            today = date.today()
            # dd/mm/YY
            flog = os.path.join(app.root_path,
                                today.strftime("%Y/%m/%d"))
            createdir(Path(flog))
            flog += '/'+session["name"]+'.log'
            # logging.basicConfig(
            #     format='%(levelname)s:%(message)s', level=logging.DEBUG)
            # logging.basicConfig(format='%(asctime)s %(message)s',
            #         datefmt='%m/%d/%Y %I:%M:%S %p')
            # logging.basicConfig(format='%(asctime)s %(message)s')

            logging.basicConfig(filename=flog, filemode='w',
                                format='%(asctime)s %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S %p',
                                level=logging.DEBUG)
            logging.info('User '+session["name_sur"]+' login success')
            logging.info(session["user_agent"])

            conn.close()
            return redirect("/")
        else:
            return render_template("login.html", info=info, error="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    return render_template("login.html", info=info, error="")


@app.route('/setocr/<int:setocr>')
def setocr(setocr):
    global info
    global ocrlot

    chkocrlot = 0
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

    info = {'totalcheked': totalcheked, 'conllection': 'civil_regis',
            'totalfile': totalfile, 'listpage': listpage, "ocrlot": session["ocrlot"], "version": version, "page": page, "ocrs": ocrs}
    return render_template('base.html',  ocrdata=[], listpage=listpage, info=info, totalcheked=totalcheked, totalfile=totalfile)


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


@app.route('/findidcard', methods=['POST', 'GET'])  #
def findidcard():
    global info
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


@app.route('/searchidcard', methods=['POST'])  #
def searchidcard():
    global info
    idc = request.form["search"]

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
            # return redirect(url_for('idcard', idcard=stridcard))
            return json.dumps(stridcard)
        else:
            return json.dumps('notfound')
        # return render_template('finddata.html', ocrdata=ocrdata, page=int(0),  info=info)
    else:
        return json.dumps('wrongID')


@app.route('/idcard/<idcard>')
def idcard(idcard):
    global info
    idcard = json.loads(idcard)
    ocrdata = conllection.find({'idcard': idcard})
    return render_template('finddata.html', ocrdata=ocrdata, info=info)


@app.route('/page/<int:page>')
def page(page):
    global info
    """Update a author."""
    # print(page)
    # listpage=totalfile//fileperpage
    skipfile = fileperpage*int(page)
    totalcheked = conllection.count_documents(
        {"ocrlot": session["ocrlot"], "checked": 1})
    info['totalcheked'] = totalcheked
    listpage = info['listpage']
    totalfile = info['totalfile']
    info["page"] = page

    #  FIND  DATA TO DICT FOR  DISPLAY
    # sortlist =
    # ocrdata = conllection.find({"ocrlot": ocrlot}).limit(
    #     fileperpage).skip(skipfile).sort({'accu_address', 1, '_id', 1}) "accu_address": 1,
    sortDic = {"accu_address": 1}  # ["index_of_lotfile", 1]

    ocrdata = conllection.find({"ocrlot": session["ocrlot"]}).limit(
        fileperpage).skip(skipfile).sort("index_of_lotfile", 1)

    # ocrdata = conllection.find({"ocrlot": ocrlot}).limit(
    #     fileperpage).skip(skipfile).sort('accu_address', 1)

    # for d in ocrdata:
    #     d['ZIPCODE'] = str(int((d['ZIPCODE']))
    #                        ) if d['ZIPCODE'] is not None else ''
    session["page"] = page
    session["listpage"] = listpage
    session["totalcheked"] = totalcheked
    session["totalfile"] = totalfile

    # print(session["name"], 'session["ocrlot"] =>',
    #       session["ocrlot"], 'page =>', page)
    logging.info('%s %s %s %s %s ', session["name"], 'session["ocrlot"] =>',
                 session["ocrlot"], 'page =>', page)

    return render_template('base.html', ocrdata=ocrdata, page=int(page), listpage=listpage, info=info, totalcheked=totalcheked, totalfile=totalfile, audit=session["name"])
    #    listpage=listpage,totalcheked=totalcheked,totalfile=totalfile)


@app.route('/addmissword', methods=['POST'])
def addmissword():
    dumdict = request.form.to_dict()

    # has IDCARD change to Append & Update
    if finddocumentcmissthai({'misword': dumdict['misword']}) == None:
        dumdict['fcount'] = 1
        x = Insertmissword(dumdict)
    return json.dumps('add')


@app.route('/toggleUpdate', methods=['POST'])
def toggleUpdate():
    dumdict = request.form.to_dict()
    myquery = {'index_of_lotfile': int(
        dumdict['index_of_lotfile']), 'ocrlot': session["ocrlot"]}
    dumdict = dict(request.form)
    # print(' index_of_lotfile ', str(
    #     dumdict['index_of_lotfile']), ' Check =', str(dumdict['checked']))
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


#  MONGO TO SQL
@ app.route('/mongo2sql', methods=['POST'])
def mongo2sql():
    global conn
    global cursor
    dumdict = request.form.to_dict()
    dumdict = dict(request.form)
    if dumdict['checked'] == '':
        info['transfer'] = 0
        return render_template('transfer.html', info=info)

    myquery = {'ocrlot': int(dumdict['ocrlot']),
               'checked': 1}
    # myquery = {'ocrlot': int(dumdict['ocrlot']),
    #            'checked': 1, 'loaddate': None}
    #  FIND  DATA TO DICT FOR  DISPLAY
    conllection = mongo.db.civil_registration
    ocrdata = conllection.find(myquery)
    logging.info('mongo2sql')
    # logging.info(len(list(ocrdata)))
    #  FIND  DATA TO DICT FOR  DISPLAY
    lcount = 0
    ucount = 0
    for doc in ocrdata:
        print('index_of_lotfile', doc['index_of_lotfile'], doc['idcard'])
        # print(doc)
        if doc['index_of_lotfile'] == 111:
            print('index_of_lotfile', doc['index_of_lotfile'], doc['idcard'])
        doc['id_card'] = doc['idcard'].replace('-', '')
        doc['status'] = 1 if doc['status'] == 'เจ้าบ้าน' else 0
        if doc['notes'] == None:
            doc['notes'] = "NULL"

        if 'บ้านกลาง' in doc['notes']:
            doc['status'] = 2
        elif 'ตาย' in doc['notes']:
            doc['status'] = 3
        if doc['status'] != 3:
            doc['notes'] = "NULL"
        else:
            doc['notes'] = "'" + doc['notes'][doc['notes'].find('ตาย'):]+"'"
            if len(doc['notes']) > 30:
                doc['notes'] = "" + doc['notes'][:30]+"'"
        doc['mixAddr'] = ('ต.' if doc['PROVINCE'] != 'กรุงเทพมหานคร' else 'แขวง') + doc['TUMBUL'] + \
            ' ' + ('อ.' if doc['PROVINCE'] !=
                   'กรุงเทพมหานคร'else 'เขต') + doc['AUMPUR']
        doc['dob'] = fnc_thatocmsdate(doc['dob'])
        doc['inputdate'] = (datetime.datetime.now()).strftime('%Y%m%d')
        strVauel = []

        SQLstr = " Update address.dbo.Data SET "

        strVauel.append(" type_address=type_address+1 ")
        strVauel.append(" status_own = " + str(doc['status']) + " ")
        strVauel.append(" address ='" + str(doc['address']) + "'")
        strVauel.append(" province = '" + doc['PROVINCE'] + "'")
        strVauel.append(" amphur = '" + doc['mixAddr'] + "'")

        if doc['ZIPCODE'] == 'None' or doc['ZIPCODE'] == '':
            if 'ทะเบียนบ้าน' in doc['address']:
                doc['ZIPCODE'] = 'None'
            else:
                doc['ZIPCODE'] = str(get_zipcode(doc))

            if doc['ZIPCODE'] != None and doc['ZIPCODE'] != 'None':
                strVauel.append(
                    "zip_code  = '" + str(doc['ZIPCODE'].replace('.0', '')) + "'")  # ตัด .0 ออก
            else:
                strVauel.append(" zip_code  = NULL ")
        else:
            strVauel.append(
                " zip_code = " + ("'" + str(doc['ZIPCODE']) + "'" if doc['ZIPCODE'] != "" else "NULL") + "")

        strVauel.append(" date_of_birth = " + doc['dob'] + " ")
        strVauel.append(" note_own = " + doc['notes'] + " ")
        strVauel.append(" father = '" + str(doc['father']) + "' ")
        strVauel.append(" mother = '" + str(doc['mother']) + "' ")
        strVauel.append(
            " state_date = 2 ,updateDTE_date=getdate(),input_date='" + doc['inputdate'] + "',Userupdate='WebApp@28' ")
        strVauel.append(" id_father ='" + str(doc['id_father']) + "' ")
        strVauel.append(" id_mother ='" + str(doc['id_mother']) + "' ")
        # print(str(doc['Name']))
        strVauel.append(" N_relation1 ='" + str(doc['Name']) + "' ")

        strWhere = " id_card = '" + doc['id_card'] + \
            "' AND type_address = 0 AND state_date <> 2  "
        # strWhere = " id_card = '" + \
        #     doc['id_card'] + "' AND userUpdate ='WebApp@28' "
        SQLstr = SQLstr + ",".join(strVauel) + " WHERE " + strWhere + " "

        try:
            print(SQLstr)
            cursor.execute(SQLstr)
            lcount += (1 if cursor.rowcount == 1 else 0)
            ucount += (1 if cursor.rowcount == 0 else 0)
            if cursor.rowcount == 1:
                myquery = {'_id': doc['_id']}
                newvalues = {"$set": {'loaddate': datetime.datetime.utcnow()}}
                try:
                    print(mongo.db.civil_registration.update_one(
                        myquery, newvalues))
                except OperationFailure as e:
                    print(
                        f"couldn't execute insert_many mylist.\n error as  {str(e)}")
        except OperationFailure as e:
            ucount += (1 if cursor.rowcount == 0 else 0)

    conn.commit()
    # cursor.execute(
    #     'SELECT count(*) FROM address.dbo.[data] WHERE convert(varchar(8),input_date,112)=%s', (datetime.datetime.now()).strftime('%Y%m%d'))
    # row = cursor.fetchone()
    info['loaddata'] = "Load data: " + \
        str(lcount) + " / " + str(ucount) + " รายการ"
    return render_template('transfer.html', info=info)
    # return json.dumps('Update ', count)
    # ocrload = mongo.db.civil_registration.find(myquery)
    # for x in ocrload:
    # return json.dumps('Update')


@ app.route('/transfer')
def transfer():
    global conn
    global cursor
    conn = pymssql.connect('192.168.1.254', 'sa', 'mymasterdb', "address")
    cursor = conn.cursor()  # as_dict=True

    conllection = mongo.db.civil_registration
    myquery = {'ocrlot': session["ocrlot"], 'checked': 1}
    totalcheked = conllection.count_documents(myquery)

    myquery = {'ocrlot': session["ocrlot"], 'loaddate': {
        "$exists": True, "$ne": None}}
    totalloaddate = conllection.count_documents(myquery)

    myquery = {'ocrlot': session["ocrlot"], 'loaddate': None}
    totalunloaddate = conllection.count_documents(myquery)
    info['transfer'] = "ข้อมูลทั้งหมด :" + str(totalcheked) + " รายการ"
    info['loaddata'] = "Load data: " + \
        str(totalloaddate) + " / " + str(totalunloaddate) + " รายการ"
    return render_template('transfer.html', info=info)

    # info['transfer'] = ' transfer' + \
    #     str(scount) + ' รายการ'+' จาก '+str(ccount) + ' รายการ'
    # return render_template('transfer.html', info=info)


def createdir(p):
    # เตรียมโฟรเดอร์เก็บไฟล์
    try:
        p.mkdir(parents=True)
    except FileExistsError as exc:
        print('Folder ' + p._str + '..........Ok ')


# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=3000)
