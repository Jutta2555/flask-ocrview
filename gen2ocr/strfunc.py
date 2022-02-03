# Load tha .word list

# G_numberinlinechk='[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
#            0       1       2    3     4     5       6     7     8     9       10
from numpy import e


KEYSLINE=['IDCARD','NAME','DOB','MOM','DAD','ADDR','DIST','UPD','NTE','EADDR','SADDR']
KEYSDICT=['idcard','name','status','notes','addr','tumbol','aumphur',
#               0      1       2        3       4        5       6
    'province','zipcode','mother','id_mother','father','id_father','filescan','filetext',
#          7        8           9       10          11      12          13          14
#          15       16          17      18          19          20      21
    'gender','nationality','dob','stlupdate','copydate','scandate','loaddate','mothernation','fathernation']
#          15       16          17      18          19          20      21       22                  23
DISTINLINE=['จ.','ต.','อ.','เขต','แขวง','กรุงเทพมหานคร']
MONTHTHAI=['มกราคม','กมภาพนธ','มนาคม','เมษายน','พฤษภาคม','มถนายน','กรกฎาคม','สงหาคม','กนยายน','ตลาคม','พฤศจกายน','ธนวาคม']
NUMTHAI='๐๑๒๓๔๕๖๗๘๙'
SARATHAI=" ี ุ ื ๊ ๋ ู ิ ้ ็แเ ัะ ์ไใ ึโ ่ ํา"
SARATHAILINE= " ี ุ ื ๊ ๋ ู ิ ้ ็ ั ์ ึ ่ ํ"
SPECAILCHAR="<>«»=.+!@#$%^&*()_+-|\{]["
NATIONAL_THCHAR='ไทยอินเดียจีน'
GENDERTHCHAR=['ชาย','ซาย','หญิง']
STATUSHOME=['เจ้าบ้าน','ผู้อาศัย','หัวหน้าครอบครัว']
DIGITINLINE='[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
PROVINCETHA=['กระบี่','กรุงเทพมหานคร','กาญจนบุรี','กาฬสินธุ์','กำแพงเพชร','ขอนแก่น','จันทบุรี','ฉะเชิงเทรา','ชลบุรี','ชัยนาท','ชัยภูมิ','ชุมพร','เชียงราย','เชียงใหม่','ตรัง','ตราด','ตาก','นครนายก','นครปฐม','นครพนม','นครราชสีมา','นครศรีธรรมราช','นครสวรรค์','นนทบุรี','นราธิวาส','น่าน','บึงกาฬ','บุรีรัมย์','ปทุมธานี','ประจวบคีรีขันธ์','ปราจีนบุรี','ปัตตานี','พระนครศรีอยุธยา','พะเยา','พังงา','พัทลุง','พิจิตร','พิษณุโลก','เพชรบุรี','เพชรบูรณ์','แพร่','ภูเก็ต','มหาสารคาม','มุกดาหาร','แม่ฮ่องสอน','ยโสธร','ยะลา','ร้อยเอ็ด','ระนอง','ระยอง','ราชบุรี','ลพบุรี','ลำปาง','ลำพูน','เลย','ศรีสะเกษ','สกลนคร','สงขลา','สตูล','สมุทรปราการ','สมุทรสงคราม','สมุทรสาคร','สระแก้ว','สระบุรี','สิงห์บุรี','สุโขทัย','สุพรรณบุรี','สุราษฎร์ธานี','สุรินทร์','หนองคาย','หนองบัวลำภู','อ่างทอง','อำนาจเจริญ','อุดรธานี','อุตรดิตถ์','อุทัยธานี','อุบลราชธานี']

def stringchrTha(s,z):
    x = " " # ช=ซ
    y = " "
    mychraum = s.maketrans(x,y,z)
    findstr=s.translate(mychraum)
    return findstr

PROVINCETHAWITHOUTSARA=list((stringchrTha(pv,SARATHAILINE)   for pv in PROVINCETHA ))

def replace_strnull_index(text,index=0, replacement=''):
    if index < 0:
        raise ValueError("index must be positive")
    elif index+len(replacement) >= len(text):
        return '%s'%(text[:index])
        # raise ValueError("index must be less than the length of the string")
    elif index == 0:
        return '%s'%(text[index+len(replacement):])

    return '%s%s'%(text[:index],text[index+len(replacement):])

def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]
def prettytxt(d, indent=0):
    strretrun=''
    for key, value in d.items():
        strretrun=strretrun +('\t' * indent + str(key))
        if isinstance(value, dict):
            strretrun=strretrun +(value, indent+1) +'\n'
        else:
            strretrun=strretrun +('\t' * (indent+1) + str(value)) +'\n'
    return strretrun
def same_engtextv2(s1,s2):
    cstr1=s1
    cstr2=''
    for c in s2:
        if c=='.': continue
        if c=='/': continue
        if c.isalpha() :return
    for idx,c in enumerate(s2):
        if idx < len(s1):
            if '1' == s1[idx] and c=='/': #replace 1 as /
                s1=s1[:idx]+s1[idx+1:]
            elif '|' == s1[idx] and c=='/': #replace 1 as /
                s1=s1[:idx]+s1[idx+1:]
            elif '!' == s1[idx] and c=='/': #replace 1 as /
                s1=s1[:idx]+s1[idx+1:]
            elif c.isdigit() :
                cstr2=cstr2+c
        elif c.isdigit() :
            cstr2=cstr2+c
    cstr1=''            
    for idx,c in enumerate(s1):
        if c.isdigit() :
            cstr1=cstr1+c

    if len(cstr1)> len(cstr2) :
        s1=cstr1
        cstr1=cstr2
        cstr2=s1

    match,i,skip  =0,0,0
    for idx,c in enumerate(cstr1):
        if c == cstr2[idx] :
            match += 1
        else:
            skip += 1
    reversecstr1=cstr1[::-1]
    reversecstr2=cstr2[::-1]
    for idx, c in enumerate(reversecstr1) :
        if c == reversecstr2[idx] :
            match += 1
        else:
            skip += 1
    if match==0 : return False
    if abs(len(s1) - len(s2)) < 2 : 
        if match >  skip:
            return True
        else:
            return False
def nowstrinforname(timestamp):
    from datetime import datetime
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime( '%d %b %Y %H:%M:%S:%f' )
    formated_date=formated_date.replace(" ", "") #
    formated_date=formated_date.replace(":", "") #    
    return formated_date
def createdir(p):
    # เตรียมโฟรเดอร์เก็บไฟล์
    try:
        p.mkdir(parents=True)
    except FileExistsError as exc:
        print('Make Folder ' + p._str + '..........Ok ') 
def writhjsonfile(txtfile,datatext):
    with open(txtfile,'a') as f: #Process :"+ custom_config +" //
        f.write(f'{datatext},')
    f.close()
def writhlogfile(txtfile,datatext,mode='a'):
    with open(txtfile,mode) as f: #Process :"+ custom_config +" //
        f.write(f'{datatext}\n')
    f.close()
def same_stringthapayachana(s1,s2):
    cstr1,cstr2='',''
    match,i,skip  =0,0,0
    for c in s1:
        if  ord(c)>=3585 and ord(c)<= 3630 :
            cstr1=cstr1 + c                            
    for c in s2:
        if  ord(c)>=3585 and ord(c)<= 3630 :
            cstr2=cstr2 + c                            
    lenstr=(len(cstr1)+len(cstr2))//2

    for c in cstr1:
        if i> len(cstr2)-1: break
        if c == cstr2[i] :
            match += 1
        else:
            skip += 1
        i+=1
    reversecstr1=cstr1[::-1]
    reversecstr2=cstr2[::-1]
    i=0
    for c in reversecstr1:
        if i> len(reversecstr2)-1: break
        if c == reversecstr2[i] :
            match += 1
            i+=1
        else:
            skip += 1

    if match>=2 : 
        if len(cstr1) == len(cstr2) : 
            match +=  len(cstr1)//2
    if match==0 : return False        
    if match > lenstr//2 and skip-2 <  match:
        return True
    else:
        return False

def stringc(s):
    x = " " # ช=ซ
    y = " "
    z = " ี ุ ื ๊ ๋ ู ิ ้ ็แเ ัะ ์ไใ ึโ ่ ํ"
    mychraum = s.maketrans(x,y,z)
    findstr=s.translate(mychraum)
    cstr=''
    for c in findstr:
        if  ord(c)>=3585 and ord(c)<= 3630 :
            cstr=cstr + c                            
    return cstr
def Nowstr_log():# Done before 160920
    from datetime import datetime, timezone, timedelta    
    # Time zone in Thailand UTC+7
    TZ = timezone(timedelta(hours = 7))
    # # Create a date object with given timezone
    d = datetime.now(tz=TZ)
    # # Reading infomation about time zone
    dx= d.isoformat(sep = " ")
    return dx
def Nowstr_slashes():# Done before 160920
    from datetime import datetime
    d= datetime.today() # + timedelta(days=1)
    # formated_date= d.strftime('%Y') 
    formated_date= d.strftime('%Y/%m/%d' ) 
    return formated_date
def convert_date(timestamp):# Done before 160920 
    from datetime import datetime
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime( '%d %b %Y %H:%M:%S:%f' )
    return formated_date
def mathchMonth(s):
    monthth=['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม',
            'สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
    if len(s)<=2 : return '' 
    for n in monthth:
        if s==n :
            return n
    for n in monthth:
        if same_stringthapayachana(stringc(s) , stringc(n)):
            return n
    return ''        
def matchnakurid(s):
    Newlinestr=''
    linestring =enumerate(s)
    for index,c in linestring:
        # found ํ  + า  แทนด้วย  ำ  
        # index 397        char:ํ   ascii:'\u0e4d'
        # index 398        char:า  ascii:'\u0e32'
        if ascii(c)=='\u0e4d' or c=='ํ' :
            auchr='ำ'
            Newlinestr=Newlinestr+auchr
            next(linestring)
        else:
            Newlinestr=Newlinestr+c
    return Newlinestr

def same_engtextv2(s1,s2):
    cstr1=s1
    cstr2=''
    for c in s2:
        if c=='.': continue
        if c=='/': continue
        if c.isalpha() :return

    for idx,c in enumerate(s2):
        if idx < len(s1):
            if '1' == s1[idx] and c=='/': #replace 1 as /
                s1=s1[:idx]+s1[idx+1:]
            elif '|' == s1[idx] and c=='/': #replace 1 as /
                s1=s1[:idx]+s1[idx+1:]
            elif '!' == s1[idx] and c=='/': #replace 1 as /
                s1=s1[:idx]+s1[idx+1:]
            elif c.isdigit() :
                cstr2=cstr2+c
        elif c.isdigit() :
            cstr2=cstr2+c
    cstr1=''            
    for idx,c in enumerate(s1):
        if c.isdigit() :
            cstr1=cstr1+c

    if len(cstr1)> len(cstr2) :
        s1=cstr1
        cstr1=cstr2
        cstr2=s1

    match,i,skip  =0,0,0
    for idx,c in enumerate(cstr1):
        if c == cstr2[idx] :
            match += 1
        else:
            skip += 1
    reversecstr1=cstr1[::-1]
    reversecstr2=cstr2[::-1]
    for idx, c in enumerate(reversecstr1) :
        if c == reversecstr2[idx] :
            match += 1
        else:
            skip += 1
    if match==0 : return False
    if abs(len(s1) - len(s2)) < 2 : 
        if match >  skip:
            return True
        else:
            return False
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def appendlist(s1,s2):
    s1.append(s2)
    return

# Retrun text samply format for get word
def format_lawocrdata(lawstring='',lawEngstring=''):
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
        dictword={w:len(w) for w in linetextlaw.split()}
        # sort Z-a word in linestring
        sort_by_value = dict(sorted(dictword.items() , reverse=True , key=lambda item: item[1])) #
        if len(sort_by_value)>0: MaxLangthChr=list(sort_by_value.values())[0]
        # `Prepair Proces word

        # หาเดือนใน บรรทัด
        MonthMatch=len(list(True for k in sort_by_value.keys() if stringchrTha(k,SARATHAILINE) in MONTHTHAI))
        # สัญชาติ
        NATIONTHMatch=len(list(True for k in sort_by_value.keys() if k in NATIONAL_THCHAR))
        # เพศ
        GenderMatch=len(list(True for k in sort_by_value.keys() if k in GENDERTHCHAR))
        # สถานะการบ้าน
        StatusMathc=len(list(True for k in sort_by_value.keys() if k in STATUSHOME))
    
        # kumwithoutsara=stringchrTha(k,SARATHAILINE)
        # MatchProvinceTH=len(list( pv for pv in PROVINCETHAWITHOUTSARA if stringchrTha(k,SARATHAILINE)[2:] in pv) for k in sort_by_value.keys() )))

        for k,v in sort_by_value.items():
            SingleChrTha,ChrNumTha,ChrSpOne,ChrSpcail,ChrNumsEng=False,False,False,False,False
            if v > 1 :# Count group of word more than 1 chr
                GrpWord += 1
                if v > 5 : # Count group of word more than 5 chr
                    if len([pv for pv in PROVINCETHAWITHOUTSARA  if stringchrTha(k,SARATHAILINE)[2:] in pv ])>0:
                        MatchProvinceTH=True

            elif v ==1 : # ตรวจอักษรโดด
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

                if ChrNumTha or ChrSpOne or ChrSpcail or ChrNumsEng or SingleChrTha:
                    if linetextlaw.find(' '+k+' ')>=0:
                        replace_text.append(' '+k+' ')
                        indexreplc.append(linetextlaw.find(' '+k+' '))                        
                    elif linetextlaw.find(' '+k)>0:
                        replace_text.append(' '+k)
                        indexreplc.append(linetextlaw.find(' '+k))
                    elif linetextlaw.find(k+' ')>=0:
                        replace_text.append(k+' ')
                        indexreplc.append(linetextlaw.find(k+' '))
            # find เลขภาษาอังกฤษ
        # lenrepc=0
        # for index ,(repc ,indexc) in enumerate(zip(replace_text,indexreplc)):
        #     if index ==0:
        #         lenrepc=len(repc)
        #         continue
        #     else:
        #         indexreplc[index]=indexreplc[index]-lenrepc
        #         lenrepc=len(repc)
            

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
            for repc ,indexc in zip(replace_text,indexreplc):
                linetextlaw=replace_strnull_index(linetextlaw,indexc,repc)
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
            if not MatchProvinceTH : # ถ้าไม่พบจังหวัดในบรรทัดนี้ จะตรวจสอบ ของบรรทัดถัดไป
                Linedata[KEYSLINE[6]]='find province'

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

        # strsplits=val.split()
        # for w in strsplits :
        #     if AtlineProcess>=2 and AtlineProcess<=4  :            
        #         if len(w)==1 : continue # drop one char not number
        #         newlinetextlaw = newlinetextlaw + w +' '
        #     else:
        #         if len(w)==1 and not w.isdigit() : continue # drop one char not number
        #         newlinetextlaw = newlinetextlaw + w +' '

        newlinetextlaw=val.strip()
        Linedata[key]=newlinetextlaw


    return Linedata

def Convertiftopng(sorce_path,dest_paht):
    import cv2
    img = cv2.imread(sorce_path)
    cv2.imwrite(dest_paht,img ) 
    pass

def Split_address(addrdict):
    dc={}
    addrdict=addrdict.replace('  ',' ' )
    ListofAddrress=addrdict.split()

    for index,addr in enumerate(ListofAddrress) :
        if int(index) > len(ListofAddrress)-3 and len(addr)<3:
            ListofAddrress.pop(index)

    if len(ListofAddrress) < 3 :
        dc['addr'] =''
        return 
    dc['addr'] =''
    for index,addr in enumerate(ListofAddrress) :
        # กรุงเทพมหานคร
        if index== len(ListofAddrress)-1 and 'กรุงเทพ' in addr:
            dc['province'] =addr
            break
        elif index== len(ListofAddrress)-2 and 'เขต' in addr:
            dc['aumphur'] =addr[3:]
        elif index== len(ListofAddrress)-3 and 'แขวง' in addr:
            dc['tumbol'] =addr[4:]
        # ต่างจังหวัด
        elif index== len(ListofAddrress)-1 :#and 'จ['' in addr:
            dc['province'] =addr[2:]
            dc['province'] =dc['province'].replace('.','')
            break
        elif index== len(ListofAddrress)-2 :#and 'อ.' in addr:
            dc['aumphur'] =addr[2:]
            dc['aumphur'] =dc['aumphur'].replace('.','')

        elif index== len(ListofAddrress)-3 :#and 'ต.' in addr:
            dc['tumbol'] =addr[2:]
            dc['tumbol'] =dc['tumbol'].replace('.','')

        elif index< len(ListofAddrress)-3:
                dc['addr'] =dc['addr'] +addr+' '
    return dc