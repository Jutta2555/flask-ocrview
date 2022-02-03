
import pandas as pd
from pymongo.message import query
from stlocrproject.gen2ocr.mongoproc import InsertPersonDictMany, InsertPersonDictOne, UpdatePersonAddr, UpdatemissPoint, Updatepersonscandb, finddocumentPerson, missworddb, personscandb
from stlocrproject.gen2ocr.strfunc import KEYSDICT, Split_address
from stlocrproject.ocrwastedicisionv1 import KEYSLINE

OcrData={}
# OcrData['IDCARD']='3-4799-00191-76-5 5701-105295-0'
# OcrData['NAME']='นายอัครวัฒน์ ตาสาย ชาย ไทย'
# OcrData['DOB']='16 พฤศจิกายน 2524 39 เจ้าบ้าน'
# OcrData['MOM']='อัญชลี 3-5799-00191-68-4 ไทย'
# OcrData['DAD']='ไสว - ไทย'
# OcrData['ADDR']='417 หมู่ 8 ต.สันทราย อะ.เมืองเชียงราย จ.เชียงราย'
# OcrData['DIST']='อําเภอเมืองเชียงราย'
# OcrData['UPD']='15 มนาคม 2561'
# OcrData['NTE']='บุคคลนีมีภูมิลําเนาอยู่ในบ้านนี'
# OcrData['EADDR']='417 V8 A.AuNnTIE AlNaUHeNTIE ALTeNe18'
# OcrData['SADDR']='417 หมู่ 8 ต.สันทราย อะ.เมืองเชียงราย จ.เชียงราย'

# KEYSLINE
# person={}
# # OcrData['IDCARD']='1-6699-00131-27-7 6505-002444-7'
# dum=OcrData[KEYSLINE[0]].split()
# if len(dum)==2:
#     person['idcard']=dum[0]
# # OcrData['NAME']='น.ส.ชิดชนก เทพอาชา หญิง ไทย'
# dum=OcrData[KEYSLINE[1]].split()
# if len(dum)==4:
#     person['name']=dum[0] +' '+dum[1]
#     person['gender']=dum[2] 
#     person['national']=dum[3] 

# # OcrData['DOB']']='16 เมษายน 2532 32 ผู้อาศัย'
# dum=OcrData[KEYSLINE[2]].split()
# if len(dum)==5:
#     person['dob']=dum[0] +' '+dum[1]+' '+dum[2]
#     person['status']=dum[4] 

# # OcrData['MOM']']='สุกัญญา - ไทย'
# dum=OcrData[KEYSLINE[3]].split()
# if len(dum)==2:
#     person['mother']=dum[0] 
#     person['motherid']='-'#dum[1] 
# if len(dum)==3:
#     person['mother']=dum[0] 
#     person['motherid']=dum[1] 

# # OcrData['DAD']='พิเนตร 3-6505-00079-12-8 ไทย'
# dum=OcrData[KEYSLINE[4]].split()
# if len(dum)==2:
#     person['farther']=dum[0] 
#     person['fartherid']='-'#dum[1] 
# if len(dum)==3:
#     person['farther']=dum[0] 
#     person['fartherid']=dum[1] 

# # OcrData['ADDR']']='45/1 หมู่ 2 ต.นครป่าหมาก อ.บางกระทุ่ม จ.พิษณุโลก'
# # OcrData['DIST']']='อําเภอบางกระทุ่ม'
# # OcrData['UPD']']='26 เมษายน 2532'
# person['update']=OcrData[KEYSLINE[7]]    

# # OcrData['NTE']='บุคคลนี้มีภูมิลําเนาอยู่ในบ้านนี้'
# person['notes']=OcrData[KEYSLINE[8]]    
# # OcrData['EADDR']='45/1 vy 2 a.uasilwain auinsenn a.Wuculan | |'
# # OcrData['SADDR']='45/1 หมู่ 2 ต.นครป่าหมาก อ.บางกระทุ่ม จ.พิษณุโลก'
# person['addr']=OcrData[KEYSLINE[10]]    

# dbdict_data=[]
# # dict2.update(dict1)
# person.update(Split_address(person['addr']))
# dictstl=person
# dbdict_data.append(dictstl)
# 1-6699-00131-27-7"
OcrData['IDCARD']='3-2399-00073-47-1 5 2201-033925-8'
# NAME	นางกุลริศา วิสุทธิแพทย์ หญิง ไทย
# DOB	16 ตุลาคม 2512 1 ผู้อาศัย
# MOM	สมจิตต์ 3-2399-00073-43-9 ไทย
# DAD	สุชาติ 3-2399-00073-51-0 ไทย
# ADDR	1/169 หมู่ 12 ต.ทําช้าง อ.เมืองจันทบุรี จ.จันทบุรี
# DIST	อําเภอเมืองจันทบุร
# UPD	2 กุมภาพันธ์ 2561
# NTE	บุคคลนี้มีภูมิลําเนาอยู่ในบ้านนี้
# EADDR	1/169 VN 12 A.MITW alNadunds a.4unus
# SADDR	1/169 หมู่ 12 ต.ทําช้าง อ.เมืองจันทบุรี จ.จันทบุรี
person={}
# OcrData['IDCARD']='1-6699-00131-27-7 6505-002444-7'
# OcrData['NAME']='น.ส.ชิดชนก เทพอาชา หญิง ไทย'
# OcrData['DOB']='16 เมษายน 2532 32 ผู้อาศัย'
# OcrData['MOM']='สุกัญญา - ไทย'
# OcrData['DAD']='พิเนตร 3-6505-00079-12-8 ไทย'
# OcrData['ADDR']='45/1 หมู่ 2 ต.นครป่าหมาก อ.บางกระทุ่ม จ.พิษณุโลก'
# # มีปัญหา 1
# OcrData['DIST']='อําเภอบางกระทุ่ม'
# OcrData['UPD']='26 เมษายน 2532'
# OcrData['NTE']='บุคคลนี้มีภูมิลําเนาอยู่ในบ้านนี้'
# OcrData['EADDR']='45/1 vy 2 a.uasilwain auinsenn a.Wuculan | |'
# OcrData['SADDR']='45/1 หมู่ 2 ต.นครป่าหมาก อ.บางกระทุ่ม จ.พิษณุโลก'
# # มีปัญหา 2 '/vsocr/ok/2021/11/02/addrocr_00000007-8.png'
# '3-4709-00111-05-5 2508-030705-6'
# 'นายวิลัย มีแสง ชาย ไทย'
# 'หนูไพร 3-4709-00111-04-7 ไทย 7'
# 'เม็ง 3-4709-00111-03-9 ไทย'
# '160/4 หมู่ 3 ต.ท่าตูม อ.ศรีมหาโพธิ จ.ปราจีนบุรี'
# 'อําเภอศรีมหาโพธิ'
# # OcrData['SADDR']='400/55 หมู่111 ต.สันทราย อะ.เมืองเชียงราย จ.เชียงราย'
# มีปัญหา 3
# 2021-11-02 14:10:49.610042+07:00	3Ocr...Processing---:/vsocr/addrocr_00000089-2 (2).tif  
OcrData['IDCARD']='1-1199-00478-20-4 1005-168070-0'
OcrData['NAME']='น.ส.นฤภร อุตรวิเชียร หญิง ไทย'
OcrData['DOB']='4 กรกฎาคม 2537 27 ผู้อาศัย'
OcrData['MOM']='สุภัชชซา 3-1002-01568-49-1 ไทย'
OcrData['DAD']='ธิรชัย 3-1101-00443-25-1 ไทย'
OcrData['ADDR']='201/471 ซอยพหลโยธิน 54/1แยก4-12(ม.อรุณนิเวศน์) แขวงคลองถนน เขตสายไหม'
OcrData['DIST']='กรุงเทพมหานคร'
OcrData['UPD']='28 เมษายน 2548'
OcrData['NTE']='บุคคลนีมีภูมิลําเนาอยู่ในบ้านนี'
OcrData['EADDR']='201/471 NALWUALEAU 54/1U2IN4-12(NATMULIAY) UNAAAAIMUY LumaAeluy'
OcrData['SADDR']='201/471 ซอยพหลโยธิน 54/1แยก4-12(ม.อรุณนิเวศน์) แขวงคลองถนน เขตสายไหม'

# def txtlinetostruct(locationg3,OcrData={},fileimg='',filetxt=''):
KEYSLINE
person={} # Stldata()
# OcrData['IDCARD']='1-6699-00131-27-7 6505-002444-7'
iddum=OcrData[KEYSLINE[0]].replace(' ','')
# if len(dum)==2:
person[KEYSDICT[0]]=iddum[:17]

# OcrData['NAME']='น.ส.ชิดชนก เทพอาชา หญิง ไทย'
dum=OcrData[KEYSLINE[1]].split()
if len(dum)==4:
    person[KEYSDICT[1]]=dum[0] +' '+dum[1]
    person[KEYSDICT[15]]=dum[2] 
    person[KEYSDICT[16]]=dum[3] 
else:
    person[KEYSDICT[1]]=''
    for i, w in enumerate(dum):
        if i > len(dum)-3: break
        person[KEYSDICT[1]]=person[KEYSDICT[1]]+ w +' '

    person[KEYSDICT[1]]=person[KEYSDICT[1]][:-1]
    person[KEYSDICT[15]]=dum[len(dum)-2] 
    person[KEYSDICT[16]]=dum[len(dum)-1] 

# OcrData['DOB']='16 เมษายน 2532 32 ผู้อาศัย'
dum=OcrData[KEYSLINE[2]].split()
if len(dum)==5:
    person[KEYSDICT[17]]=dum[0] +' '+dum[1]+' '+dum[2]
# OcrData['DOB']='เมษายน 2532 32 ผู้อาศัย'
elif len(dum)==4:
    person[KEYSDICT[17]]=dum[0] +' '+dum[1]
elif len(dum)==3:
    person[KEYSDICT[17]]=dum[0] 
person[KEYSDICT[2]]=dum[len(dum)-1] 

# OcrData['MOM']='สุกัญญา - ไทย'
dum=OcrData[KEYSLINE[3]].split()
if len(dum)==2:
    person[KEYSDICT[9]]=dum[0] 
    person[KEYSDICT[10]]='-'#dum[1] 
    person[KEYSDICT[22]]=dum[len(dum)-1]  

if len(dum)==3:
    person[KEYSDICT[9]]=dum[0] 
    person[KEYSDICT[10]]=dum[1] 
    person[KEYSDICT[22]]=dum[len(dum)-1]

# OcrData['DAD']='พิเนตร 3-6505-00079-12-8 ไทย'
dum=OcrData[KEYSLINE[4]].split()
if len(dum)==2:
    person[KEYSDICT[11]]=dum[0] 
    person[KEYSDICT[12]]='-'#dum[1] 
    person[KEYSDICT[23]]=dum[len(dum)-1]
if len(dum)==3:
    person[KEYSDICT[11]]=dum[0] 
    person[KEYSDICT[12]]=dum[1] 
    person[KEYSDICT[23]]=dum[len(dum)-1]

# OcrData['UPD']='26 เมษายน 2532'
person[KEYSDICT[18]]=OcrData[KEYSLINE[7]]

# OcrData['NTE']='บุคคลนี้มีภูมิลําเนาอยู่ในบ้านนี้'
person[KEYSDICT[3]]=OcrData[KEYSLINE[8]]

# OcrData['EADDR']='45/1 vy 2 a.uasilwain auinsenn a.Wuculan | |'
# OcrData['SADDR']='45/1 หมู่ 2 ต.นครป่าหมาก อ.บางกระทุ่ม จ.พิษณุโลก'
# OcrData['ADDR']='45/1 หมู่ 2 ต.นครป่าหมาก อ.บางกระทุ่ม จ.พิษณุโลก'
person[KEYSDICT[4]]=OcrData[KEYSLINE[10]]

# person.update(Split_address(person[KEYSDICT[4]]))
person[KEYSDICT[8]]=0
# person[KEYSDICT[13]]=fileimg
# person[KEYSDICT[14]]=filetxt
# person[KEYSDICT[14]]=filetxt
    # person[KEYSDICT[20]]= datetime.datetime.utcnow()#Nowstr_log() # datetime.datetime.isoformat(sep = " ") #.utcnow()











# dum=OcrData[KEYSLINE[0]].split()
# if len(dum)==2:
#     person[KEYSDICT[0]]=dum[0]
# # OcrData['NAME']='น.ส.ชิดชนก เทพอาชา หญิง ไทย'
# dum=OcrData[KEYSLINE[1]].split()
# if len(dum)==4:
#     person[KEYSDICT[1]]=dum[0] +' '+dum[1]
#     person[KEYSDICT[15]]=dum[2] 
#     person[KEYSDICT[16]]=dum[3] 

# # OcrData['DOB']']='16 เมษายน 2532 32 ผู้อาศัย'
# dum=OcrData[KEYSLINE[2]].split()
# if len(dum)==5:
#     person[KEYSDICT[17]]=dum[0] +' '+dum[1]+' '+dum[2]
#     person[KEYSDICT[2]]=dum[4] 

# # OcrData['MOM']']='สุกัญญา - ไทย'
# dum=OcrData[KEYSLINE[3]].split()
# if len(dum)==2:
#     person[KEYSDICT[9]]=dum[0] 
#     person[KEYSDICT[10]]='-'#dum[1] 
# if len(dum)==3:
#     person[KEYSDICT[9]]=dum[0] 
#     person[KEYSDICT[10]]=dum[1] 
# dum=OcrData[KEYSLINE[4]].split()
# if len(dum)==2:
#     person[KEYSDICT[11]]=dum[0] 
#     person[KEYSDICT[12]]='-'#dum[1] 
# if len(dum)==3:
#     person[KEYSDICT[11]]=dum[0] 
#     person[KEYSDICT[12]]=dum[1] 
# person[KEYSDICT[18]]=OcrData[KEYSLINE[7]]    

# person[KEYSDICT[3]]=OcrData[KEYSLINE[8]]    

# person[KEYSDICT[4]]=OcrData[KEYSLINE[10]]    
dum='1 พฤศจิกายน 2511 52 ผู้อาศัย 0'.split()
if len(dum[len(dum)-1])==1:
    dum.pop(len(dum)-1)

# person.update(Split_address(person[KEYSDICT[4]]))
# dictstl=person
# # dbdict_data.append(dictstl)

# qrystr={KEYSLINE[0]:person[KEYSLINE[0]]}
# x=InsertPersonDictOne(dictstl)
# import os
# person=personscandb()
# for row in person:
#     myquery={"_id":row['_id']}
#     oldfile=row['filescan']
#     idcard=row['idcard']
#     idcard=idcard.replace('-','')
#     idcard=idcard.replace('=','')
#     newfile=oldfile.replace(' ','')
#     newfile=newfile.replace('(','')
#     newfile=newfile.replace(')','')
#     newfile=newfile.replace('addrocr_00000',idcard+'-')
#     os.rename(oldfile,newfile)

#     newvalues={"$set": {"filescan":newfile[1:],"filetext":row['filetext'][1:]}}
#     Updatepersonscandb(myquery,newvalues)

    # x=InsertPersonDictOne(dictstl)



# x=InsertPersonDictMany(dbdict_data)    
# print(x.inserted_ids)


# linetextlaw='1 กุมภาพันธ์2504 สูทิน60 ผู้อาศัย'
# linetextlaw='2ตุลาคม2522 42 ผู้อาศัย'
# #=['มกราคม','กมภาพนธ','มนาคม','เมษายน','พฤษภาคม','มถนายน','กรกฎาคม','สงหาคม','กนยายน','ตลาคม','พฤศจกายน','ธนวาคม']

# # แก้คำผิดในสายสตรืิง ภาษาไทยจากฐานข้อมูลใน Mongo and Hit+=1  ---------------------------------------------
# listofmissworddb=missworddb()
# # use 'generator FOR LINE NAME '
# reslut=(next((item for item in listofmissworddb if item["misword"] in linetextlaw), None))
# # if reslut != None :
#     linetextlawxx=linetextlaw.replace(reslut['misword'],reslut['rghword'])
#     myquery = { "misword": reslut['misword'] }
#     # { $inc: {<field1>: <amount1>, <field2>: <amount2>, ...} }
#     newvalues = { "$inc": { "fcount": 1 } }
#     UpdatemissPoint(myquery,newvalues )
# print(linetextlawxx)    


# ขยับวันที่ ที่มีตัวเลขติดกับเดือน---------------------------------------------
# import re
# editdate=(re.findall(r"(\d{1,}[ก,ม,เ,พ,ส,ต,พ,ธ])",linetextlaw))
# if len(editdate)>0:
#     print(linetextlaw.replace(editdate[0],editdate[0][0]+' '+editdate[0][1]) )
# else:
#     print(linetextlaw)
# editdate=(re.findall(r"([ม,น,์]\d{4,})",linetextlaw))
# if len(editdate)>0:
#     print(linetextlaw.replace(editdate[0],editdate[0][0]+' '+editdate[0][1:]) )
# else:
#     print(linetextlaw)

#               0           1           2           3       4           5       6
# KEYSDICT=['id_card','new_name','status_own','note_own','address','tumbol','amphur',
#          7        8           9       10          11      12          13          14
#     'province','zipcode','mother','id_mother','father','id_father','filescan','filetext',
#          15       16          17      18          19          20      21
#      'gender','nationality','dob','stlupdate','copydate','scandate','loaddate']

# OcrData['DAD']='พิเนตร 3-6505-00079-12-8 ไทย'
                