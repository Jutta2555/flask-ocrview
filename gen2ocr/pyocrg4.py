import datetime
import json
import os
import sys
from pathlib import Path

import cv2
import pandas as pd
import pytesseract
from stlocrproject.gen2ocr.mongoproc import (InsertPersonDictOne,
                                             UpdatemissPoint, UpdatePersonAddr,
                                             finddocumentPerson, locdb,
                                             missworddb)
from stlocrproject.gen2ocr.strfuncg2 import (DIGITINLINE, DISTINLINE,
                                             GENDERTHCHAR, KEYSDICT, KEYSLINE,
                                             MONTHTHAI, NATIONAL_THCHAR,
                                             NUMTHAI, PROVINCETHAWITHOUTSARA,
                                             SARATHAI, SARATHAILINE,
                                             SPECAILCHAR, STATUSHOME,
                                             Convertiftopng, Nowstr_log,
                                             Nowstr_slashes, Split_address,
                                             createdir, 
                                             isEnglish, matchnakurid,
                                             mathchMonth, 
                                             replace_strnull_index,
                                             same_engtextv2,
                                             same_stringthapayachana, stringc,
                                             stringchrTha )

# InsertPersonDictMany,
# from stlocrproject.ocrstlscan_debug import writhfiletxt
PAYANCHANATHA='กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ'

killfile=False
typefile=None
pwdroot='/vsocr/GHB20' #'folder workpath txtfilealgorthm
if len(sys.argv)==1 :
    pwdpicocr='/vsocr/GHB20' #' folder for tif scan in txtfilealgorthm
else:
    # /path/to/folder/ True 1  # folder for tif scan in algorthm & ลบไฟล์ต้นฉบับ  & typefile รูปแบบรับรอง
    # /path/to/folder/ False 0 # folder for tif scan in algorthm & เก็บไฟล์ต้นฉบับ & typefile รูปแบบไม่รับรอง 
    pwdpicocr=sys.argv[1]     
    killfile=sys.argv[2]     
    typefile=sys.argv[3]     

bufferlen=20 # Buffer file cut to store in database
locationg3= pd.DataFrame(list(locdb())) # data Location for Zipcode 
missword= missworddb() # data wrong word usaully found in OCR Method 

# สร้างโฟรเดอร์เก็บไฟล์ผลการสแกน
FOLDERRESULT=os.path.join(pwdpicocr,"ok",Nowstr_slashes())    
createdir(Path(FOLDERRESULT))

logprocname='logg2proc.txt' # LOG DATA Temporaly
JSONDATAPAHT='ocrdata_debug.json' # LOG DATA Temporaly
custom_config='--psm 0 --psm 6' # OCR PSM ARG ='--psm 0 --psm 6'

def same_stringthapayachanaG2(s1,s2):
    cstr1,cstr2='',''
    match,skip  =0,0
    cstr1=[c for c in s1 if c in PAYANCHANATHA]
    cstr1=''.join(cstr1)
    cstr2=[c for c in s2 if c in PAYANCHANATHA]
    cstr2=''.join(cstr2)

    lenstr=(len(cstr1)+len(cstr2))//2

    listchk=['match' if c1==c2 else 'skip' for (c1,c2) in zip(cstr1,cstr2) ]
    reversecstr1=cstr1[::-1]
    reversecstr2=cstr2[::-1]
    listchkrevs=['match' if c1==c2 else 'skip' for (c1,c2) in zip(reversecstr1,reversecstr2) ]
    match=listchkrevs.count('match')+listchk.count('match')
    skip=listchkrevs.count('skip')+listchk.count('skip')

    if match>=2 : 
        if len(cstr1) == len(cstr2) : 
            match +=  len(cstr1)//2
    if match==0 : return False
    if match > lenstr//2 and skip-2 <  match:
        return True
    else:
        return False
def stringcG2(s):
    x = " " # ช=ซ
    y = " "
    z = " ี ุ ื ๊ ๋ ู ิ ้ ็แเ ัะ ์ไใ ึโ ่ ํ"
    mychraum = s.maketrans(x,y,z)
    findstr=s.translate(mychraum)
    cstr=[c for c in findstr if c in PAYANCHANATHA]
    cstr=''.join(cstr)
    return cstr    

def txtlinetostructG2(OcrData={}):
    import re
    global locationg3
    person={} # Stldata()

    iddum=OcrData[KEYSLINE[0]]#.replace(' ','')
    # IDCARD	00 3-3419-00797-99-4 7606-003746-1    
    newiddum=''
    for c in iddum:
        if c.isdigit() or c=='-' or c==' ':
            newiddum=newiddum+c

    idstart=re.findall(r"(\d{1,}[-]\d{4,}[-]\d{5,}[-]\d{2,}[-]\d{1,})",newiddum) 
    if len(idstart)==1:
        person[KEYSDICT[0]]=idstart[0]
    else:
        print(f"Error IDCARD {newiddum}")
        person[KEYSDICT[0]]=''

    # OcrData['NAME']='น.ส.ชิดชนก เทพอาชา หญิง ไทย ก.' 
    person[KEYSDICT[16]]=next(fnd for fnd in OcrData[KEYSLINE[1]].split() if fnd in NATIONAL_THCHAR)
    genderat=next({fnd:index} for index,fnd in enumerate(OcrData[KEYSLINE[1]].split()) if fnd in GENDERTHCHAR ) #else None
    if genderat != None :
        person[KEYSDICT[15]]=list(genderat.keys())[0]
        namepstr=list((fnd) for index, fnd in enumerate(OcrData[KEYSLINE[1]].split()) if index < list(genderat.values())[0])
        person[KEYSDICT[1]]=' '.join(namepstr)
    else:   
        person[KEYSDICT[1]]=OcrData[KEYSLINE[1]]
        person[KEYSDICT[15]]=''
    
    
    # OcrData['DOB']='16 เมษายน 2532 32 ผู้อาศัย'
    m=next(([index,w,mathchMonth(w)] for index ,w in  enumerate( OcrData[KEYSLINE[2]].split()) if mathchMonth(w)!='' ),None)
    y=next(([index,w] for index ,w in  enumerate( OcrData[KEYSLINE[2]].split()) if w.isdigit() and len(w)==4 ),None)
    s=next(([index,w] for index ,w in  enumerate( OcrData[KEYSLINE[2]].split()) if w in STATUSHOME  ),None)
    if m is not None:
        if m[0]==0 :
            if y is not None:
                person[KEYSDICT[17]]=y[1]
        else:
            if y is not None:
                person[KEYSDICT[17]]=' '.join((OcrData[KEYSLINE[2]].split()[m[0]-1],m[2],y[1]))
            else:
                person[KEYSDICT[17]]=' '.join( (OcrData[KEYSLINE[2]].split()[m[0]-1],m[2]))
    if s is not None:
        person[KEYSDICT[2]]=s[1]


    # OcrData['MOM']='สุกัญญา - ไทย'
    atnameposi=0
    s=next(([index,w] for index ,w in  enumerate(OcrData[KEYSLINE[3]].split()) if w in NATIONAL_THCHAR and index >0 ),None)
    id=next(([index,w] for index ,w in  enumerate(OcrData[KEYSLINE[3]].split()) if len(re.findall(r"(\d{1,}[-]\d{4,}[-]\d{5,}[-]\d{2,}[-]\d{1,})",w))>0 ),None)

    if id is None and len(re.findall(r"\d{4,}",OcrData[KEYSLINE[3]]) )>0:
        id=[[index,w] for index,w  in enumerate(OcrData[KEYSLINE[3]].split()) if len(re.findall(r"\d{1,}",w))>0 ]
        atnameposi=id[0][0]
        person[KEYSDICT[10]]=id[0][1]+id[1][1]
    elif id is not None:
        atnameposi=id[0]
        person[KEYSDICT[10]]=id[1]

    if s is not None: 
        if atnameposi==0:atnameposi=s[0]
        person[KEYSDICT[22]]=s[1]    
    elif atnameposi==0:
        atnameposi=len(OcrData[KEYSLINE[3]].split())-1
    nmom=[w for index ,w in  enumerate(OcrData[KEYSLINE[3]].split()) if index < atnameposi]   
    if nmom is not None:person[KEYSDICT[9]]=' '.join(nmom)


    # OcrData['DAD']='พิเนตร 3-6505-00079-12-8 ไทย'
    atnameposi=0
    s=next(([index,w] for index ,w in  enumerate(OcrData[KEYSLINE[4]].split()) if w in NATIONAL_THCHAR and index >0 ),None)
    id=next(([index,w] for index ,w in  enumerate(OcrData[KEYSLINE[4]].split()) if len(re.findall(r"(\d{1,}[-]\d{4,}[-]\d{5,}[-]\d{2,}[-]\d{1,})",w))>0 ),None)

    if id is None and len(re.findall(r"\d{4,}",OcrData[KEYSLINE[4]]) )>0:
        id=[[index,w] for index,w  in enumerate(OcrData[KEYSLINE[4]].split()) if len(re.findall(r"\d{1,}",w))>0 ]
        atnameposi=id[0][0]
        person[KEYSDICT[12]]=id[0][1]+id[1][1]
    elif id is not None:
        atnameposi=id[0]
        person[KEYSDICT[12]]=id[1]

    if s is not None: 
        if atnameposi==0:atnameposi=s[0]
        person[KEYSDICT[23]]=s[1]    
    elif atnameposi==0:
        atnameposi=len(OcrData[KEYSLINE[3]].split())-1
    nmom=[w for index ,w in  enumerate(OcrData[KEYSLINE[4]].split()) if index < atnameposi]   
    if nmom is not None:person[KEYSDICT[11]]=' '.join(nmom)


    # OcrData['UPD']='26 เมษายน 2532'
    m=next(([index,w,mathchMonth(w)] for index ,w in  enumerate( OcrData[KEYSLINE[7]].split()) if mathchMonth(w)!='' ),None)
    y=next(([index,w] for index ,w in  enumerate( OcrData[KEYSLINE[7]].split()) if w.isdigit() and len(w)==4 ),None)
    if m is not None:
        if m[0]==0 :
            if y is not None:
                person[KEYSDICT[18]]=y[1]
        else:
            if y is not None:
                person[KEYSDICT[18]]=' '.join((OcrData[KEYSLINE[7]].split()[m[0]-1],m[2],y[1]))
            else:
                person[KEYSDICT[18]]=' '.join( (OcrData[KEYSLINE[7]].split()[m[0]-1],m[2]))

    # OcrData['NTE']='บุคคลนี้มีภูมิลําเนาอยู่ในบ้านนี้'
    person[KEYSDICT[3]]=OcrData[KEYSLINE[8]]

    # OcrData['DIST']='กรุงเทพมหานคร'    
    person[KEYSDICT[4]]=OcrData[KEYSLINE[10]]

    person.update(Split_address(OcrData[KEYSLINE[10]]))
    person[KEYSDICT[8]]=0
    # person[KEYSDICT[13]]=fileimg[1:]
    # person[KEYSDICT[14]]=filetxt[1:]
    # person[KEYSDICT[20]]= datetime.datetime.utcnow()#Nowstr_log() # datetime.datetime.isoformat(sep = " ") #.utcnow()


    # persondata[KEYSDICT[]]=find_zipcode(persondata,locationg3)
        # เตรียมข้อมูล zipcode ชื่อจังหวัด  อำเภอ และตำบล ให้พร้อม
    print('Prov :',person[KEYSDICT[7]])
    print('aumphur :',person[KEYSDICT[6]])
    print('tumbol :',person[KEYSDICT[5]])
    # ตรวจสอบ จ อ ต พร้อมกัน  
    is_Prov= locationg3[locationg3.PROVINCE.str.contains(person[KEYSDICT[7]]) & locationg3.AUMPUR.str.contains(person[KEYSDICT[6]]) & locationg3.TUMBUL.str.contains(person[KEYSDICT[5]])]
    if len(is_Prov.index) != 0: # พบ จัวหวัด และอำเภอ และ ตำบล Bingo
            for index, row in is_Prov.iterrows(): 
                print('F_Prov :',row["PROVINCE"])
                print('F_aumphur :',row["AUMPUR"])
                print('F_tumbol :',row["TUMBUL"])
                person[KEYSDICT[7]]=row["PROVINCE"] #is_Prov.PROVINCE.values[0][:]
                person[KEYSDICT[6]]=row["AUMPUR"] #is_Prov.AUMPUR.values[0][:]
                person[KEYSDICT[5]]=row["TUMBUL"]
                person[KEYSDICT[8]]=int(row["ZIPCODE"])
    else: # ไม่พบ จังหวัด และอำเภอ ตำบล ที่มีส่วนประกอบใกล้เคียง
        print('Find ocrstring province')
        findstr=stringcG2(person[KEYSDICT[7]])   # province
        is_Prov= locationg3[ locationg3.ocrstring.str.contains(findstr) ]

        for index, row in is_Prov.iterrows(): # หาจาก ฟังชั่น ตัวอักษรเหมือน จากข้อมูลทั้งหมดsame_stringthapayachanaG2(person[KEYSDICT[5]],row["TUMBUL"]) and  same_stringthapayachanaG2(person[KEYSDICT[6]],row["AUMPUR"]) and
            if  same_stringthapayachanaG2(person[KEYSDICT[5]],row["TUMBUL"]) and same_stringthapayachanaG2(person[KEYSDICT[6]],row["AUMPUR"]) and  same_stringthapayachanaG2(person[KEYSDICT[7]],row["PROVINCE"])  :
                print('Found _Prov :',row["PROVINCE"],row["AUMPUR"],row["TUMBUL"])
                print('F_Prov :',row["PROVINCE"])
                print('F_aumphur :',row["AUMPUR"])
                print('F_tumbol :',row["TUMBUL"])
                person[KEYSDICT[7]]=row["PROVINCE"] #i
                person[KEYSDICT[6]]=row["AUMPUR"] #is
                person[KEYSDICT[5]]=row["TUMBUL"]
                person[KEYSDICT[8]]=int(row["ZIPCODE"])
                break # # end
        if person[KEYSDICT[8]]!='' :  #
            print('Find ocrstring amphur')    
            findstr=stringcG2( person[KEYSDICT[6]])   # 'amphur
            is_Prov= locationg3[ locationg3.ocrstring.str.contains(findstr) ]
            for index, row in is_Prov.iterrows(): # หาจาก ฟังชั่น ตัวอักษรเหมือน จากข้อมูลทั้งหมดsame_stringthapayachanaG2(person[KEYSDICT[5]],row["TUMBUL"]) and  same_stringthapayachanaG2(person[KEYSDICT[6]],row["AUMPUR"]) and
                if  same_stringthapayachanaG2(person[KEYSDICT[5]],row["TUMBUL"]) and same_stringthapayachanaG2(person[KEYSDICT[6]],row["AUMPUR"]) and  same_stringthapayachanaG2(person[KEYSDICT[7]],row["PROVINCE"])  :
                    print('F_Prov :',row["PROVINCE"])
                    print('F_aumphur :',row["AUMPUR"])
                    print('F_tumbol :',row["TUMBUL"])                                
                    person[KEYSDICT[7]]=row["PROVINCE"] #i
                    person[KEYSDICT[6]]=row["AUMPUR"] #is
                    person[KEYSDICT[5]]=row["TUMBUL"]
                    person[KEYSDICT[8]]=int(row["ZIPCODE"])
                    break # # end
            if person[KEYSDICT[8]]!='' :#
                print('Find ocrstring tumbol')    
                findstr=stringcG2( person[KEYSDICT[5]])   # 'tumbol
                is_Prov= locationg3[ locationg3.ocrstring.str.contains(findstr) ]
                for index, row in is_Prov.iterrows(): # หาจาก ฟังชั่น ตัวอักษรเหมือน จากข้อมูลทั้งหมดsame_stringthapayachanaG2(person[KEYSDICT[5]],row["TUMBUL"]) and  same_stringthapayachanaG2(person[KEYSDICT[6]],row["AUMPUR"]) and
                    if  same_stringthapayachanaG2(person[KEYSDICT[5]],row["TUMBUL"]) and same_stringthapayachanaG2(person[KEYSDICT[6]],row["AUMPUR"]) and  same_stringthapayachanaG2(person[KEYSDICT[7]],row["PROVINCE"])  :
                        print('F_Prov :',row["PROVINCE"])
                        print('F_aumphur :',row["AUMPUR"])
                        print('F_tumbol :',row["TUMBUL"])                                
                        person[KEYSDICT[7]]=row["PROVINCE"] #i
                        person[KEYSDICT[6]]=row["AUMPUR"] #is
                        person[KEYSDICT[5]]=row["TUMBUL"]
                        person[KEYSDICT[8]]=int(row["ZIPCODE"])
                        break # # end
    return person

# Retrun text samply format for get word
def format_lawocrdataM(lawstring='',lawEngstring=''):
    import re
    print('')
    Linedata={
        KEYSLINE[0]:'',
        KEYSLINE[1]:'',
        KEYSLINE[2]:'',
        KEYSLINE[3]:'',
        KEYSLINE[4]:'',
        KEYSLINE[5]:'',
        KEYSLINE[6]:'',
        KEYSLINE[7]:'',
        KEYSLINE[8]:'',
        KEYSLINE[9]:'',
        KEYSLINE[10]:''
    }
    # Prepair data for process
    processstring=matchnakurid(lawstring)
    Aprocessstring=processstring.splitlines() 
    AlawEngstring=lawEngstring.splitlines()
    AtlineProcess=0
    addresslineinthai=0
    #  ='3-1012-01933-36-0 1005-234909-8'
    for linenumber, linetextlaw in enumerate(Aprocessstring ) :
        SingleChrTha, ChrNumsEng,MatchProvinceTH,NumFour,ChrNumTha,NumfourandDash,NATIONTHMatch,ChrSpOne,ChrSpcail,MonthMatch,HomeNumber,GenderMatch,StatusMathc=False,False,False,False,False,False,False,False,False,False,False ,False ,False
        MaxLangthChr,GrpWord,CountChrinLine,DistCount=0,0,0,0
        replace_text,indexreplc=[],[]
        # `Prepair Count static ChrNumTha,WordInThai
        # LINE LEANGH ความยาวสายสตริงในบรรทัด
        CountChrinLine= len(linetextlaw) 
        AtlineProcess=linenumber+1
        if len(linetextlaw)<3: continue
        # รูปแบบสายสตริง ที่ประกอบด้วยตัวเล มีขึดหน้า 4 ตัวเลข ติดกัน และเป็น eng
        if len(re.findall(r"([-]\d{4,})",linetextlaw)) >0: 
            NumfourandDash=True
        if len(re.findall(r"(\d{4,})",linetextlaw)) >0: 
            NumFour=True
        # Find Distric in Thailand
        if AtlineProcess>=4 and Linedata[KEYSLINE[5]]=='':
            listDistCount= list( 1 for d in DISTINLINE if d in linetextlaw )
            DistCount=len(listDistCount)
            # ค้นหาบ้านเลขที่อยู่
            if len(re.findall(r"(\d)",linetextlaw))>0: 
                HomeNumber=True 
            elif 'เบียนบ้านกลาง' in linetextlaw :
                HomeNumber=True

        # Make Dict of word and lenofword  
        listword=[w for w in linetextlaw.split()]
        MaxLangthChr=max([ len(l) for l in linetextlaw.split() if len(l) > MaxLangthChr])

        # หาเดือนใน บรรทัด
        
        MonthMatch=len(list(True for k in listword if stringchrTha(k,SARATHAILINE) in MONTHTHAI))
        # สัญชาติ
        NATIONTHMatch=len(list(True for k in listword if k in NATIONAL_THCHAR))
        # เพศ
        GenderMatch=len(list(True for k in listword if k in GENDERTHCHAR))
        # สถานะการบ้าน
        StatusMathc=len(list(True for k in listword if k in STATUSHOME))
    
        # kumwithoutsara=stringchrTha(k,SARATHAILINE)
        # MatchProvinceTH=len(list( pv for pv in PROVINCETHAWITHOUTSARA if stringchrTha(k,SARATHAILINE)[2:] in pv) for k in sort_by_value.keys() )))
        tood=0
        for k in listword :
        # for k,v in sort_by_value.items():
            SingleChrTha,ChrNumTha,ChrSpOne,ChrSpcail,ChrNumsEng=False,False,False,False,False
            if len(k) > 1 :# Count group of word more than 1 chr
                GrpWord += 1

            elif len(k) ==1 : # ตรวจอักษรโดด
                if k in SARATHAI :
                    ChrSpOne=True                   
                elif k in SPECAILCHAR :
                    ChrSpcail=True                   
                elif k in NUMTHAI :
                    ChrNumTha=True
                elif k.isdigit():
                    ChrNumsEng=True
                elif ord(k) in range(3585,3630):
                    SingleChrTha=True
                
                #  find start at end of position last find
                if ChrNumTha or ChrSpOne or ChrSpcail or ChrNumsEng or SingleChrTha:
                    if linetextlaw.find( ' '+k+' ')>=0:
                        tood=linetextlaw.find( ' '+k+' ',tood+1,len(linetextlaw))
                        replace_text.append(' '+k+' ')
                        indexreplc.append(tood)
                    elif linetextlaw.find(' '+k)>0:
                        tood=linetextlaw.find( ' '+k,tood+1,len(linetextlaw))
                        replace_text.append(' '+k)
                        indexreplc.append(tood)
                    elif linetextlaw.find(k+' ')>=0:
                        # tood=linetextlaw.find( k+' ',tood,len(linetextlaw))+1
                        replace_text.append(k+' ')
                        indexreplc.append(0)
            # find เลขภาษาอังกฤษ

            

        # ตัดสินใจเลือกบรรทัด****        #  INPUT  LAWDATA  TO INLINEFORMAT ='3-1012-01933-36-0 1005-234909-8'
        if NumfourandDash and  DistCount ==0: # บรรทัด ประกอบด้วยรูปแบบเลขไอดี
            if AtlineProcess < 2 : # line  ID CARD
                tood=0
                for repc ,indexc in zip(replace_text,indexreplc):

                    linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                    tood=tood+len(repc)

                Linedata[KEYSLINE[0]]=linetextlaw.replace('=','-')
                Linedata[KEYSLINE[0]]=Linedata[KEYSLINE[0]].replace('.','')
                continue

            # Cash Father and Mother line has  ID CARD 
            elif AtlineProcess > 3 and Linedata[KEYSLINE[3]]=='' and NATIONTHMatch : # line Mom และบรรทัดแม่ต้องว่าง  กรณีมีไอดี พ่อ หรือ แม่
                # ระวังไอดี แม่ไม่มี แต่ว่าบรรทัดเป็นของพ่อ **
                tood=0
                for repc ,indexc in zip(replace_text,indexreplc):
                    linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                    tood=tood+len(repc)
                Linedata[KEYSLINE[3]]=linetextlaw
                continue
            elif  Linedata[KEYSLINE[3]]!='' or NATIONTHMatch  : # บรรทัด Father
                tood=0
                for repc ,indexc in zip(replace_text,indexreplc):
                    linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                    tood=tood+len(repc)
                Linedata[KEYSLINE[4]]=linetextlaw
                continue

        elif  AtlineProcess<7 and GrpWord > 3 and MaxLangthChr >= 5 and (NATIONTHMatch or GenderMatch) :# บรรทัดชื่อ สัญชาต เพศ
            tood=0
            for repc ,indexc in zip(replace_text,indexreplc):
                linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                tood=tood+len(repc)
            Linedata[KEYSLINE[1]]=linetextlaw
            if ' ซาย ' in linetextlaw: 
                Linedata[KEYSLINE[1]]=linetextlaw.replace(' ซาย ',' ชาย ')
            else:
                Linedata[KEYSLINE[1]]=linetextlaw
            continue

        elif  AtlineProcess<9 and GrpWord >= 3 and MaxLangthChr > 5 and (MonthMatch or NumFour or StatusMathc) and Linedata[KEYSLINE[2]]=='' : # บรรทัด วันเกิด  สถานะอาศัย
            tood=0
            for repc ,indexc in zip(replace_text,indexreplc):
                if repc.strip().isdigit(): continue # ตัดสินใจ Not ตัด วัน 
                linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                tood=tood+len(repc)
            editdate=(re.findall(r"(\d{1,}[ก,ม,เ,พ,ส,ต,พ,ธ])",linetextlaw)) # ตัดวัน แยกตัวเลขติดออกจากเดือน
            if len(editdate)>0:
                Linedata[KEYSLINE[2]]=(linetextlaw.replace(editdate[0],editdate[0][0]+' '+editdate[0][1]) )
            else:
                Linedata[KEYSLINE[2]]=(linetextlaw)

            editdate=(re.findall(r"([ม,น,์]\d{4,})",linetextlaw)) # ตัดปี แยกตัวเลขติดออกจากเดือน
            if len(editdate)>0:
                Linedata[KEYSLINE[2]]=(linetextlaw.replace(editdate[0],editdate[0][0]+' '+editdate[0][1:]) )
            else:
                Linedata[KEYSLINE[2]]=(linetextlaw)

            continue

        elif  AtlineProcess<11 and (NATIONTHMatch) and Linedata[KEYSLINE[2]]!='' :# บรรทัด แม่ พ่อ ไม่มีไอดี และ ไทย
            tood=0
            for repc ,indexc in zip(replace_text,indexreplc):
                linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                tood=tood+len(repc)
            if  Linedata[KEYSLINE[3]]=='' : 
                Linedata[KEYSLINE[3]]=linetextlaw # บรรทัด แม่
            elif Linedata[KEYSLINE[4]]=='': #  Linedata[KEYSLINE[3]]=='' :
                Linedata[KEYSLINE[4]]=linetextlaw  # บรรทัด Father
            continue

        elif  AtlineProcess > 5 and DistCount >= 1 and HomeNumber and MaxLangthChr >=5 : # บรรทัดที่อยู่
            tood=0
            for repc ,indexc in zip(replace_text,indexreplc):
                if repc.strip().isdigit(): continue # ตัดสินใจ Not ตัด วัน 
                linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                tood=tood+len(repc)
            Linedata[KEYSLINE[5]]=linetextlaw

            reslut=[[item['misword'],item['rghword']] for item in missword if item["misword"] in Linedata[KEYSLINE[5]]]
            for item in reslut:
                Linedata[KEYSLINE[5]]=ReplaceMissword(Linedata[KEYSLINE[5]],item[0],item[1],'misword')

            for index ,k in enumerate(Linedata[KEYSLINE[5]].split()):
                if index > len(Linedata[KEYSLINE[4]])-3: 
                    if len([pv for pv in PROVINCETHAWITHOUTSARA  if stringchrTha(k,SARATHAILINE)[2:] in pv ])==0:
                        Linedata[KEYSLINE[6]]='find province'

            #         MatchProvinceTH=True
            # if not MatchProvinceTH : # ถ้าไม่พบจังหวัดในบรรทัดนี้ จะตรวจสอบ ของบรรทัดถัดไป
            #     Linedata[KEYSLINE[6]]='find province'

            addresslineinthai=AtlineProcess-1           
            #ตรวจต้องพบตัวเลขที่บ้าน เทียบกับ OCR EHG 
            if len(Aprocessstring)!=len(AlawEngstring): 
                if len(re.findall(r"(\d{3,})",linetextlaw)) >0: 
                    keychk=re.findall(r"(\d{3,})",linetextlaw)
                elif len(re.findall(r"(\d{2,})",linetextlaw)) >0: 
                    keychk=re.findall(r"(\d{2,})",linetextlaw)
                else:
                    keychk=re.findall(r"(\d{1,})",linetextlaw)
                for index,lineeng in enumerate( AlawEngstring):
                    if index>4 :
                        if keychk[0] in lineeng or keychk[len(keychk)-1] in lineeng:
                            Linedata[KEYSLINE[9]]=lineeng
                            break

                if Linedata[KEYSLINE[9]]=='':
                    print ("not match addrees")
                continue

            else:
                # AlawEngstring[9]
                Linedata[KEYSLINE[9]]=AlawEngstring[addresslineinthai]
            continue
                
        elif Linedata[KEYSLINE[5]]!='' and Linedata[KEYSLINE[6]]=='find province' and AtlineProcess > 5 and MaxLangthChr > 5 and GrpWord < 4: # บรรทัด เจ้าของข้อมูล ทร. สำรองที่อยู่2
            tood=0
            for repc ,indexc in zip(replace_text,indexreplc):
                linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                tood=tood+len(repc)
            Linedata[KEYSLINE[5]]=Linedata[KEYSLINE[5]] +' '+ linetextlaw
            Linedata[KEYSLINE[6]]=''
            continue

        elif Linedata[KEYSLINE[5]]!='' and Linedata[KEYSLINE[6]]=='' and AtlineProcess > 5 and MaxLangthChr > 6 and GrpWord < 3: # บรรทัด เจ้าของข้อมูล ทร.
            tood=0
            for repc ,indexc in zip(replace_text,indexreplc):
                if repc.strip().isdigit(): continue # ตัดสินใจ Not ตัด วัน 
                linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                tood=tood+len(repc)
            Linedata[KEYSLINE[6]]=linetextlaw
            continue

        elif Linedata[KEYSLINE[6]]!='' and AtlineProcess > 5 and MaxLangthChr < 15  and (MonthMatch or NumFour)  : # บรรทัด วันที่ข้อมูลล่าสุด.
            tood=0
            for repc ,indexc in zip(replace_text,indexreplc):
                if repc.strip().isdigit(): continue # ตัดสินใจ Not ตัด วัน 
                linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                tood=tood+len(repc)
            Linedata[KEYSLINE[7]]=linetextlaw
            continue

        elif  AtlineProcess > 6 and MaxLangthChr > 20 and GrpWord < 6: # บรรทัด [Notes of data] Linedata[KEYSLINE[7]]!='' and
            tood=0
            for repc ,indexc in zip(replace_text,indexreplc):
                if repc.strip().isdigit(): continue # ตัดสินใจ Not ตัด วัน 
                linetextlaw=replace_strnull_index(linetextlaw,indexc-tood,repc)
                tood=tood+len(repc)
            Linedata[KEYSLINE[8]]=linetextlaw
            continue

    #  Clean  one chr and find Word in Thai DB
    AtlineProcess=0
    newlinetextlaw,liststrtha='',''
    for key, val in Linedata.items():
        #               1       2     3      4     5    6      7     8      9     10        11
        # KEYSLINE=['IDCARD','NAME','DOB','MOM','DAD','ADDR','DIST','UPD','NTE','EADDR','SADDR']
        #               0       1     2     3     4     5       6      7    8       9      10
        if Linedata[key]=='':
            print(f" Line data {key}  not found")
        AtlineProcess+= 1
        newlinetextlaw=''        
        if AtlineProcess==6  :  # บรรทัด ทร.ADDR
            xaddr=val.split()
            if len(xaddr) < 3 : # ตัดออกจากที่อยู่ที่มีช่องว่าง
                newlinetextlaw=newlinetextlaw +val +'\n'
            for index,addr in enumerate(xaddr) :
                if not ( index > len(xaddr)-3 and len(addr)<3):
                    liststrtha=liststrtha+addr +' '
            liststrtha=liststrtha.strip()
            Linedata[key]=liststrtha
            continue

        if AtlineProcess==10  : # บรรทัด ทร.EADDR
            Linedata[key]=val
            liststrtha=liststrtha.replace('!','/')
            liststrtha=liststrtha.replace('|','/')
            liststrtha=liststrtha.split()
            liststrtha3=val.split()            
            n=0
            strthanew=''            
            
            for l in list(liststrtha):
                if  re.search(DIGITINLINE,l) is not None: # ตรวจต้องพบตัวเลข
                    if  isEnglish(l) : #0==liststrtha.index(l) and
                        for j in range(n,len(liststrtha3)-1,1):

                            if same_engtextv2(l,liststrtha3[j]):
                               
                                if '9' in l[0] and '0' in liststrtha3[j][0]:
                                    print('skip 9 = 0')
                                else:
                                    liststrtha3[j]=liststrtha3[j].replace(".", "/")
                                    if l==liststrtha3[j] :
                                        n=j+1
                                        break
                                    l=l.replace(l,liststrtha3[j])
                                    n=j+1
                                    break
                    else:
                        homno=''
                        for k in l:
                            if k.isdigit() : homno=homno+k
                        for j in range(n,len(liststrtha3)-1):
                            if n!=0 : break
                            if  re.search(DIGITINLINE,liststrtha3[j]) is not None: # ตรวจต้องพบตัวเลข
                                for m in liststrtha3[j]:
                                    if  m in homno :  
                                        liststrtha3[j]=liststrtha3[j].replace(".", "/")
                                        l=l.replace(l,liststrtha3[j])
                                        n=j+1
                                        break
                strthanew=strthanew +l +' '

            strthanew=strthanew.strip()
            Linedata[KEYSLINE[10]]=strthanew
            break
 
        newlinetextlaw=val.strip()
        Linedata[key]=newlinetextlaw

    return Linedata

def OcrdatatoFormantJson(ocrdict,killfile=False):

    OcrData={}
    OcrData=format_lawocrdataM(ocrdict[KEYSDICT[25]],ocrdict[KEYSDICT[26]])


    for i in range(5):# ตรวจสอบว่ามีคำผิดในฐาน ที่พบประจำ เพื่อแก้ไข 
        if i==0 or i==2: continue
        reslut=[[item['misword'],item['rghword']] for item in missword if item["misword"] in OcrData[KEYSLINE[i]]]
        for item in reslut:
            OcrData[KEYSLINE[i]]=ReplaceMissword(OcrData[KEYSLINE[i]],item[0],item[1],'misword')


    filename =os.path.join(FOLDERRESULT,os.path.basename(ocrdict[KEYSDICT[13]]))    
    filePng =filename.replace('.tif','.png')
    filePng=filePng.replace(' ','')
    filePng=filePng.replace('(','')
    filePng=filePng.replace(')','')
    Convertiftopng(ocrdict[KEYSDICT[13]],filePng)

    persondata=txtlinetostructG2(OcrData )
    
    if killfile :os.remove(ocrdict[KEYSDICT[13]])
    ocrdict[KEYSDICT[13]]=filePng

    return persondata

def Nowstrjson_log():
    a_datetime = datetime.datetime.now()
    formatted_datetime = a_datetime.isoformat()
    return json.dumps(formatted_datetime) #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def Ocr_JsonFiles(entrypath,killfile=False): 
    if entrypath=='' :return '',''

    import json
    global JSONDATAPAHT

    ocrdict={}
    jsonocrsummary={}
    jsonocrsummary['ocrdata']=[]
    jsonocrpage={}
    jsonocrpage['ocrdata']=[]
    pageindex=0
    JSONDATAPAHT=os.path.join(FOLDERRESULT,os.path.basename(JSONDATAPAHT))
    for index,imgstl in enumerate(entrypath) :
        print (f'file {index} : {imgstl}')
        img = cv2.imread(imgstl)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # add new record of image
        ocrdict[KEYSDICT[13]]=imgstl # 'filescan'
        ocrdict[KEYSDICT[24]]=index # 'index_file'
        ocrdict[KEYSDICT[20]]=json.dumps(datetime.datetime.now().isoformat())  # 'scandate'Nowstrjson_log()

        ocrdict[KEYSDICT[25]]=(pytesseract.image_to_string(gray, lang='tha', config=custom_config) )# 
        ocrdict[KEYSDICT[26]]=(pytesseract.image_to_string(gray, lang='eng', config=custom_config) )# 

        dumdict=OcrdatatoFormantJson(ocrdict,False)
        ocrdict.update(dumdict.items())

        jsonocrpage['ocrdata'].append(ocrdict)

        jsonocrsummary['ocrdata'].append(ocrdict)
        ocrdict={}
        dumdict={}

        if ((index+1) % bufferlen)==0 or index >= len(entrypath)-1 :# Process  in Buffer
            pageindex+=1
            jsondatafilepage=JSONDATAPAHT.replace('.json',f'_{pageindex}.json')
            with open(jsondatafilepage,'w',encoding='utf8') as f:
                f.write(json.dumps(jsonocrpage,ensure_ascii=False))
            jsonocrpage['ocrdata']=[]
      
    jsondatafilepage=JSONDATAPAHT.replace('.json',f'_total.json')
    with open(jsondatafilepage,'w',encoding='utf8') as f:
        f.write(json.dumps(jsonocrsummary,ensure_ascii=False))
    pass

    # return mainthaocr ,mainengocr

def ReplaceMissword(OcrDataLine,misword,rghword,keyname):
    OcrDataLine=OcrDataLine.replace(misword,rghword)
    myquery = { keyname: misword }
    newvalues = { "$inc": { "fcount": 1 } }
    UpdatemissPoint(myquery,newvalues )    
    return OcrDataLine
def txtlinetostruct(OcrData={},fileimg='',filetxt=''):
    import re
    global locationg3
    person={} # Stldata()

    iddum=OcrData[KEYSLINE[0]]#.replace(' ','')
    # IDCARD	00 3-3419-00797-99-4 7606-003746-1    
    newiddum=''
    for c in iddum:
        if c.isdigit() or c=='-' or c==' ':
            newiddum=newiddum+c

    idstart=re.findall(r"(\d{1,}[-]\d{4,}[-]\d{5,}[-]\d{2,}[-]\d{1,})",newiddum) 
    if len(idstart)==1:
        person[KEYSDICT[0]]=idstart[0]
    else:
        print(f"Error IDCARD {newiddum}")
        person[KEYSDICT[0]]=''



    # OcrData['NAME']='น.ส.ชิดชนก เทพอาชา หญิง ไทย ก.' 
    person[KEYSDICT[16]]=next(fnd for fnd in OcrData[KEYSLINE[1]].split() if fnd in NATIONAL_THCHAR)
    genderat=next({fnd:index} for index,fnd in enumerate(OcrData[KEYSLINE[1]].split()) if fnd in GENDERTHCHAR ) #else None
    if genderat != None :
        person[KEYSDICT[15]]=list(genderat.keys())[0]
        namepstr=list((fnd) for index, fnd in enumerate(OcrData[KEYSLINE[1]].split()) if index < list(genderat.values())[0])
        person[KEYSDICT[1]]=' '.join(namepstr)
    else:   
        person[KEYSDICT[1]]=OcrData[KEYSLINE[1]]
        person[KEYSDICT[15]]=''
    
    
    # OcrData['DOB']='16 เมษายน 2532 32 ผู้อาศัย'
    m=next(([index,w,mathchMonth(w)] for index ,w in  enumerate( OcrData[KEYSLINE[2]].split()) if mathchMonth(w)!='' ),None)
    y=next(([index,w] for index ,w in  enumerate( OcrData[KEYSLINE[2]].split()) if w.isdigit() and len(w)==4 ),None)
    s=next(([index,w] for index ,w in  enumerate( OcrData[KEYSLINE[2]].split()) if w in STATUSHOME  ),None)
    if m is not None:
        if m[0]==0 :
            if y is not None:
                person[KEYSDICT[17]]=y[1]
        else:
            if y is not None:
                person[KEYSDICT[17]]=' '.join((OcrData[KEYSLINE[2]].split()[m[0]-1],m[2],y[1]))
            else:
                person[KEYSDICT[17]]=' '.join( (OcrData[KEYSLINE[2]].split()[m[0]-1],m[2]))
    if s is not None:
        person[KEYSDICT[2]]=s[1]


    # OcrData['MOM']='สุกัญญา - ไทย'
    atnameposi=0
    s=next(([index,w] for index ,w in  enumerate(OcrData[KEYSLINE[3]].split()) if w in NATIONAL_THCHAR ),None)
    id=next(([index,w] for index ,w in  enumerate(OcrData[KEYSLINE[3]].split()) if len(re.findall(r"(\d{1,}[-]\d{4,}[-]\d{5,}[-]\d{2,}[-]\d{1,})",w))>0 ),None)

    if id is None and len(re.findall(r"\d{4,}",OcrData[KEYSLINE[3]]) )>0:
        id=[[index,w] for index,w  in enumerate(OcrData[KEYSLINE[3]].split()) if len(re.findall(r"\d{1,}",w))>0 ]
        atnameposi=id[0][0]
        person[KEYSDICT[10]]=id[0][1]+id[1][1]
    elif id is not None:
        atnameposi=id[0]
        person[KEYSDICT[10]]=id[1]

    if s is not None: 
        if atnameposi==0:atnameposi=s[0]
        person[KEYSDICT[22]]=s[1]    
    elif atnameposi==0:
        atnameposi=len(OcrData[KEYSLINE[3]].split())-1
    nmom=[w for index ,w in  enumerate(OcrData[KEYSLINE[3]].split()) if index < atnameposi]   
    if nmom is not None:person[KEYSDICT[9]]=' '.join(nmom)


    # OcrData['DAD']='พิเนตร 3-6505-00079-12-8 ไทย'
    atnameposi=0
    s=next(([index,w] for index ,w in  enumerate(OcrData[KEYSLINE[4]].split()) if w in NATIONAL_THCHAR ),None)
    id=next(([index,w] for index ,w in  enumerate(OcrData[KEYSLINE[4]].split()) if len(re.findall(r"(\d{1,}[-]\d{4,}[-]\d{5,}[-]\d{2,}[-]\d{1,})",w))>0 ),None)

    if id is None and len(re.findall(r"\d{4,}",OcrData[KEYSLINE[4]]) )>0:
        id=[[index,w] for index,w  in enumerate(OcrData[KEYSLINE[4]].split()) if len(re.findall(r"\d{1,}",w))>0 ]
        atnameposi=id[0][0]
        person[KEYSDICT[12]]=id[0][1]+id[1][1]
    elif id is not None:
        atnameposi=id[0]
        person[KEYSDICT[12]]=id[1]

    if s is not None: 
        if atnameposi==0:atnameposi=s[0]
        person[KEYSDICT[23]]=s[1]    
    elif atnameposi==0:
        atnameposi=len(OcrData[KEYSLINE[3]].split())-1
    nmom=[w for index ,w in  enumerate(OcrData[KEYSLINE[4]].split()) if index < atnameposi]   
    if nmom is not None:person[KEYSDICT[11]]=' '.join(nmom)


    # OcrData['UPD']='26 เมษายน 2532'
    m=next(([index,w,mathchMonth(w)] for index ,w in  enumerate( OcrData[KEYSLINE[7]].split()) if mathchMonth(w)!='' ),None)
    y=next(([index,w] for index ,w in  enumerate( OcrData[KEYSLINE[7]].split()) if w.isdigit() and len(w)==4 ),None)
    if m is not None:
        if m[0]==0 :
            if y is not None:
                person[KEYSDICT[18]]=y[1]
        else:
            if y is not None:
                person[KEYSDICT[18]]=' '.join((OcrData[KEYSLINE[7]].split()[m[0]-1],m[2],y[1]))
            else:
                person[KEYSDICT[18]]=' '.join( (OcrData[KEYSLINE[7]].split()[m[0]-1],m[2]))

    # OcrData['NTE']='บุคคลนี้มีภูมิลําเนาอยู่ในบ้านนี้'
    person[KEYSDICT[3]]=OcrData[KEYSLINE[8]]

    # OcrData['DIST']='กรุงเทพมหานคร'    
    person[KEYSDICT[4]]=OcrData[KEYSLINE[10]]

    person.update(Split_address(OcrData[KEYSLINE[10]]))
    person[KEYSDICT[8]]=0
    person[KEYSDICT[13]]=fileimg[1:]
    person[KEYSDICT[14]]=filetxt[1:]
    # person[KEYSDICT[20]]= datetime.datetime.utcnow()#Nowstr_log() # datetime.datetime.isoformat(sep = " ") #.utcnow()


    # persondata[KEYSDICT[]]=find_zipcode(persondata,locationg3)
        # เตรียมข้อมูล zipcode ชื่อจังหวัด  อำเภอ และตำบล ให้พร้อม
    print('Prov :',person[KEYSDICT[7]])
    print('aumphur :',person[KEYSDICT[6]])
    print('tumbol :',person[KEYSDICT[5]])
    # ตรวจสอบ จ อ ต พร้อมกัน  
    is_Prov= locationg3[locationg3.PROVINCE.str.contains(person[KEYSDICT[7]]) & locationg3.AUMPUR.str.contains(person[KEYSDICT[6]]) & locationg3.TUMBUL.str.contains(person[KEYSDICT[5]])]
    if len(is_Prov.index) != 0: # พบ จัวหวัด และอำเภอ และ ตำบล Bingo
            for index, row in is_Prov.iterrows(): 
                print('F_Prov :',row["PROVINCE"])
                print('F_aumphur :',row["AUMPUR"])
                print('F_tumbol :',row["TUMBUL"])
                person[KEYSDICT[7]]=row["PROVINCE"] #is_Prov.PROVINCE.values[0][:]
                person[KEYSDICT[6]]=row["AUMPUR"] #is_Prov.AUMPUR.values[0][:]
                person[KEYSDICT[5]]=row["TUMBUL"]
                person[KEYSDICT[8]]=int(row["ZIPCODE"])
    else: # ไม่พบ จังหวัด และอำเภอ ตำบล ที่มีส่วนประกอบใกล้เคียง
        print('Find ocrstring province')
        findstr=stringc(person[KEYSDICT[7]])   # province
        is_Prov= locationg3[ locationg3.ocrstring.str.contains(findstr) ]

        for index, row in is_Prov.iterrows(): # หาจาก ฟังชั่น ตัวอักษรเหมือน จากข้อมูลทั้งหมดsame_stringthapayachana(person[KEYSDICT[5]],row["TUMBUL"]) and  same_stringthapayachana(person[KEYSDICT[6]],row["AUMPUR"]) and
            # print('_Prov :',row["PROVINCE"],'_aumphur :',row["AUMPUR"],'_tumbol :',row["TUMBUL"])
            if  same_stringthapayachana(person[KEYSDICT[5]],row["TUMBUL"]) and same_stringthapayachana(person[KEYSDICT[6]],row["AUMPUR"]) and  same_stringthapayachana(person[KEYSDICT[7]],row["PROVINCE"])  :
                print('Found _Prov :',row["PROVINCE"],row["AUMPUR"],row["TUMBUL"])
                print('F_Prov :',row["PROVINCE"])
                print('F_aumphur :',row["AUMPUR"])
                print('F_tumbol :',row["TUMBUL"])
                person[KEYSDICT[7]]=row["PROVINCE"] #i
                person[KEYSDICT[6]]=row["AUMPUR"] #is
                person[KEYSDICT[5]]=row["TUMBUL"]
                person[KEYSDICT[8]]=int(row["ZIPCODE"])
                break # # end
        if person[KEYSDICT[8]]!='' :  #
            print('Find ocrstring amphur')    
            findstr=stringc( person[KEYSDICT[6]])   # 'amphur
            is_Prov= locationg3[ locationg3.ocrstring.str.contains(findstr) ]
            for index, row in is_Prov.iterrows(): # หาจาก ฟังชั่น ตัวอักษรเหมือน จากข้อมูลทั้งหมดsame_stringthapayachana(person[KEYSDICT[5]],row["TUMBUL"]) and  same_stringthapayachana(person[KEYSDICT[6]],row["AUMPUR"]) and
                # print('_Prov :',row["PROVINCE"],'_aumphur :',row["AUMPUR"],'_tumbol :',row["TUMBUL"])
                if  same_stringthapayachana(person[KEYSDICT[5]],row["TUMBUL"]) and same_stringthapayachana(person[KEYSDICT[6]],row["AUMPUR"]) and  same_stringthapayachana(person[KEYSDICT[7]],row["PROVINCE"])  :
                    print('F_Prov :',row["PROVINCE"])
                    print('F_aumphur :',row["AUMPUR"])
                    print('F_tumbol :',row["TUMBUL"])                                
                    person[KEYSDICT[7]]=row["PROVINCE"] #i
                    person[KEYSDICT[6]]=row["AUMPUR"] #is
                    person[KEYSDICT[5]]=row["TUMBUL"]
                    person[KEYSDICT[8]]=int(row["ZIPCODE"])
                    break # # end
            if person[KEYSDICT[8]]!='' :#
                print('Find ocrstring tumbol')    
                findstr=stringc( person[KEYSDICT[5]])   # 'tumbol
                is_Prov= locationg3[ locationg3.ocrstring.str.contains(findstr) ]
                for index, row in is_Prov.iterrows(): # หาจาก ฟังชั่น ตัวอักษรเหมือน จากข้อมูลทั้งหมดsame_stringthapayachana(person[KEYSDICT[5]],row["TUMBUL"]) and  same_stringthapayachana(person[KEYSDICT[6]],row["AUMPUR"]) and
                    # print('_Prov :',row["PROVINCE"],'_aumphur :',row["AUMPUR"],'_tumbol :',row["TUMBUL"])
                    if  same_stringthapayachana(person[KEYSDICT[5]],row["TUMBUL"]) and same_stringthapayachana(person[KEYSDICT[6]],row["AUMPUR"]) and  same_stringthapayachana(person[KEYSDICT[7]],row["PROVINCE"])  :
                        print('F_Prov :',row["PROVINCE"])
                        print('F_aumphur :',row["AUMPUR"])
                        print('F_tumbol :',row["TUMBUL"])                                
                        person[KEYSDICT[7]]=row["PROVINCE"] #i
                        person[KEYSDICT[6]]=row["AUMPUR"] #is
                        person[KEYSDICT[5]]=row["TUMBUL"]
                        person[KEYSDICT[8]]=int(row["ZIPCODE"])
                        break # # end
    return person

def main():
    ocrfiles=[]

    dir_entries = sorted(Path(pwdpicocr).iterdir(), key=os.path.getmtime)
    nextstep = False
    # keep list of file ocr
    for entry in dir_entries: # OCR_filev2() returns
        if entry.is_file() and  (".tif" in entry.name ): #or ".jpg" in entry.name  
            # # for audit tif one by one'addrocrg1_00000085.tif', ,'addrocrg1_00000110.tif'
            listoffiles=['addrGHB_00000192.tif','addrGHB_00000065.tif','addrocrg1_00000116.tif','addrocrg1_00000013-5.tif' ] 
            #เลขที่บ้าน หาย
            if  entry.name in listoffiles :
                nextstep = True
            if nextstep == False :continue    
            print(f'-{Nowstr_log()}--- {entry.name}\t Ocr.......Processing: ')
            ocrfiles.append(entry._str)
        nextstep = False

    if len(ocrfiles)>0 : Ocr_JsonFiles(ocrfiles )  # Ocr files list
    return

if __name__ == '__main__' :
    main()

