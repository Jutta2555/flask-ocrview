import datetime
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
from stlocrproject.gen2ocr.strfunc import (KEYSDICT, KEYSLINE, Convertiftopng,
                                           Nowstr_log, Nowstr_slashes,
                                           Split_address, createdir,
                                           format_lawocrdata, mathchMonth,
                                           prettytxt, same_stringthapayachana,
                                           stringc, writhlogfile)

# InsertPersonDictMany,
# from stlocrproject.ocrstlscan_debug import writhfiletxt

killfile=False
pwdroot='/vsocr' #'folder workpath txtfilealgorthm
if len(sys.argv)==1 :
    pwdpicocr='/vsocr' #' folder for tif scan in txtfilealgorthm
else:
    pwdpicocr=sys.argv[1]     
    killfile=sys.argv[2]     

bufferlen=20 # Buffer file cut to store in database
locationg3= pd.DataFrame(list(locdb())) # data Location for Zipcode 
missword= missworddb() # data wrong word usaully found in OCR Method 

# สร้างโฟรเดอร์เก็บไฟล์ผลการสแกน
folderresult=os.path.join(pwdpicocr,"ok",Nowstr_slashes())    
createdir(Path(folderresult))
logprocname='logg2proc.txt' # LOG DATA Temporaly
custom_config='--psm 0 --psm 6' # OCR PSM ARG ='--psm 0 --psm 6'


def OcrdatatoMongo(thatexts,engtexts,ocrfiles,killfile=False):
    logproc=None
    logproc=os.path.join(folderresult,os.path.basename(logprocname))   
    # thatexts,engtexts=Ocr_Files(ocrfiles,custom_config)
    for index , (thatext,engtext,FilesTiff) in enumerate(zip(thatexts,engtexts,ocrfiles)):
        OcrData={}
        OcrData=format_lawocrdata(thatext,engtext)
        if OcrData[KEYSLINE[0]]=='' or OcrData[KEYSLINE[1]]=='': 
            writhlogfile(logproc,f'{Nowstr_log()}\t{index}Ocr*****Error*****Processing***** :{FilesTiff}  ','a')
            writhlogfile(logproc,prettytxt(OcrData) ,'a')
            
            continue
        if not KEYSLINE[0] in OcrData or not KEYSLINE[10] in OcrData:
            print(f" Line '{KEYSLINE[0]}' OR Line {KEYSLINE[10]} not in OCR {FilesTiff}")
            continue
        # use 'generator FOR LINE NAME '
        # reslut=(next((item for item in missword if item["misword"] in OcrData[KEYSLINE[0]]), None))
        # if reslut != None :
        #     OcrData[KEYSLINE[0]]=ReplaceMissword(OcrData[KEYSLINE[0]],reslut['misword'],reslut['rghword'],'misword')

        reslut=(next((item for item in missword if item["misword"] in OcrData[KEYSLINE[1]]), None))
        if reslut != None :
            OcrData[KEYSLINE[1]]=ReplaceMissword(OcrData[KEYSLINE[1]],reslut['misword'],reslut['rghword'],'misword')

        reslut=(next((item for item in missword if item["misword"] in OcrData[KEYSLINE[3]]), None))
        if reslut != None :
            OcrData[KEYSLINE[3]]=ReplaceMissword(OcrData[KEYSLINE[3]],reslut['misword'],reslut['rghword'],'misword')

        reslut=(next((item for item in missword if item["misword"] in OcrData[KEYSLINE[4]]), None))
        if reslut != None :
            OcrData[KEYSLINE[4]]=ReplaceMissword(OcrData[KEYSLINE[4]],reslut['misword'],reslut['rghword'],'misword')

        reslut=(next((item for item in missword if item["misword"] in OcrData[KEYSLINE[5]]), None))
        if reslut != None :
            OcrData[KEYSLINE[5]]=ReplaceMissword(OcrData[KEYSLINE[5]],reslut['misword'],reslut['rghword'],'misword')

        # csv_dict_data.append(OcrData)

        filename =os.path.join(folderresult,os.path.basename(FilesTiff))    
        filePng =filename.replace('.tif','.png')
        filePng=filePng.replace(' ','')
        filePng=filePng.replace('(','')
        filePng=filePng.replace(')','')
        Convertiftopng(FilesTiff,filePng)

        writhlogfile(logproc,f'{Nowstr_log()}\t{index}Ocr...Processing---:{FilesTiff}  ','a')
        writhlogfile(logproc,prettytxt(OcrData) ,'a')

        persondata=txtlinetostruct(OcrData ,filePng,logproc)
        writhlogfile(logproc,prettytxt(persondata) ,'a')
        # dbdict_data.append(persondata)  use Mongo DB 
        qrystr={KEYSDICT[0]:persondata[KEYSDICT[0]]}
        if finddocumentPerson(qrystr)!=None: # has IDCARD chage to Append & Update
            UpdatePersonAddr(persondata)
        else:
            x=InsertPersonDictOne(persondata)
        
        if killfile :os.remove(FilesTiff)

    pass

# เก็บข้อมูลOCR tha & Eng return string2
def Ocr_Files(entrypath): 
    if entrypath=='' :return '',''
    mainthaocr=[] 
    mainengocr=[]
    ocrfiles=[]
    for index,imgstl in enumerate(entrypath) :
        print (f'file {index} : {imgstl}')
        img = cv2.imread(imgstl)
        mainthaocr.append(pytesseract.image_to_string(img, lang='tha', config=custom_config) )# 
        mainengocr.append(pytesseract.image_to_string(img, lang='eng', config=custom_config) )# 
        ocrfiles.append(imgstl)
        # remainder = 31 % 10
        if (index % bufferlen)==0 or index >= len(entrypath)-1 :# Process  in Buffer
            OcrdatatoMongo(mainthaocr ,mainengocr,ocrfiles,killfile)
            mainthaocr=[] 
            mainengocr=[]
            ocrfiles=[]
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
    KEYSLINE
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

    # OcrData['NAME']='น.ส.ชิดชนก เทพอาชา หญิง ไทย'
    dum=OcrData[KEYSLINE[1]].split()
    if len(dum[len(dum)-1])==1:
        dum.pop(len(dum)-1)    
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
        person[KEYSDICT[17]]=dum[0] +' '+ mathchMonth(dum[1])+' '+dum[2]
    # OcrData['DOB']='เมษายน 2532 32 ผู้อาศัย'
    elif len(dum)==4:
        person[KEYSDICT[17]]= mathchMonth(dum[0]) +' '+ dum[1]
    elif len(dum)==3:
        person[KEYSDICT[17]]=dum[0] 
    person[KEYSDICT[2]]=dum[len(dum)-1] 

    # OcrData['MOM']='สุกัญญา - ไทย'
    dum=OcrData[KEYSLINE[3]].split()
    # MOM	บุญธรรม 3-1102-00505-96-7 ไทย 5
    # DAD	สุชิน ไทย
    # MOM	อูมิลา อินเดีย
    # DAD	กริสนา โมฮัน อินเดีย    
    # DAD	บุญรักษ์ 3-4502-00435-61-3 ไทย 0    
    for index,singlew in enumerate(dum) :
        if int(index) > len(dum)-1 and len(singlew)<2:
            dum.pop(index)
    if len(dum)==2:
        person[KEYSDICT[9]]=dum[0] 
        person[KEYSDICT[10]]='-'#dum[1] 
        person[KEYSDICT[22]]=dum[len(dum)-1]  
    elif len(dum)==3:
        person[KEYSDICT[9]]=dum[0] 
        person[KEYSDICT[10]]=dum[1] 
        person[KEYSDICT[22]]=dum[len(dum)-1]
    elif len(dum)==4:
        person[KEYSDICT[9]]=dum[0]  +' '+dum[1]
        person[KEYSDICT[10]]=dum[2] 
        person[KEYSDICT[22]]=dum[len(dum)-1]


    # OcrData['DAD']='พิเนตร 3-6505-00079-12-8 ไทย'
    dum=OcrData[KEYSLINE[4]].split()
    for index,singlew in enumerate(dum) :
        if int(index) > len(dum)-1 and len(singlew)<2:
            dum.pop(index)    
    if len(dum)==2:
        person[KEYSDICT[11]]=dum[0] 
        person[KEYSDICT[12]]='-'#dum[1] 
        person[KEYSDICT[23]]=dum[len(dum)-1]
    if len(dum)==3:
        person[KEYSDICT[11]]=dum[0] 
        person[KEYSDICT[12]]=dum[1] 
        person[KEYSDICT[23]]=dum[len(dum)-1]
    elif len(dum)==4:
        person[KEYSDICT[11]]=dum[0]  +' '+dum[1]
        person[KEYSDICT[12]]=dum[2] 
        person[KEYSDICT[23]]=dum[len(dum)-1]

    # OcrData['UPD']='26 เมษายน 2532'
    dum=OcrData[KEYSLINE[7]].split()
    if len(dum)==3:
        person[KEYSDICT[18]]=dum[0]+' '+ mathchMonth(dum[1])+' '+dum[2]
    # OcrData['UPD']='เมษายน 2532'
    elif len(dum)==2:
        person[KEYSDICT[18]]= mathchMonth(dum[0]) +' '+ dum[1]
        # person[KEYSDICT[18]]=OcrData[KEYSLINE[7]]

    # OcrData['NTE']='บุคคลนี้มีภูมิลําเนาอยู่ในบ้านนี้'
    person[KEYSDICT[3]]=OcrData[KEYSLINE[8]]

    # OcrData['EADDR']='45/1 vy 2 a.uasilwain auinsenn a.Wuculan | |'
    # OcrData['SADDR']='45/1 หมู่ 2 ต.นครป่าหมาก อ.บางกระทุ่ม จ.พิษณุโลก'
    # OcrData['ADDR']='45/1 หมู่ 2 ต.นครป่าหมาก อ.บางกระทุ่ม จ.พิษณุโลก'

    # OcrData['ADDR']='201/471 ซอยพหลโยธิน 54/1แยก4-12(ม.อรุณนิเวศน์) แขวงคลองถนน เขตสายไหม'
    # OcrData['DIST']='กรุงเทพมหานคร'    
    person[KEYSDICT[4]]=OcrData[KEYSLINE[10]]

    person.update(Split_address(OcrData[KEYSLINE[10]]))
    person[KEYSDICT[8]]=0
    person[KEYSDICT[13]]=fileimg[1:]
    person[KEYSDICT[14]]=filetxt[1:]
    person[KEYSDICT[20]]= datetime.datetime.utcnow()#Nowstr_log() # datetime.datetime.isoformat(sep = " ") #.utcnow()


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
            # # for audit tif one by one'addrocrg1_00000023-1.tif', ,'addrocrg1_00000110.tif'
            # listoffiles=['addrocrg1_00000031.tif','addrocrg1_00000033.tif','addrocrg1_00000038-1.tif','addrocrg1_00000043-1.tif' ]            
            # if  entry.name in listoffiles :
            #     nextstep = True
            # if nextstep == False :continue    
            print(f'-{Nowstr_log()}--- {entry.name}\t Ocr.......Processing: ')
            ocrfiles.append(entry._str)
        nextstep = False

    if len(ocrfiles)>0 : Ocr_Files(ocrfiles )  # Ocr files list
    return

if __name__ == '__main__' :
    main()




    # global pwdpicocr
    # global pwdroot
    # dbdict_data=[] # DICT FOR MONGODB    
    # csv_dict_data=[] # DICT FOR Text log


        # Wordin thai EDIT OcrData as dict  
        # import pandas as pd
        # locationg3= pd.DataFrame(list(locdb()))
        # # missword=missworddb()
        # missword= missworddb()

        
        # for index , (thatext,engtext,FilesTiff) in enumerate(zip(thatexts,engtexts,ocrfiles)):
        #     OcrData={}
        #     OcrData=format_lawocrdata(thatext,engtext)
        #     if not KEYSLINE[0] in OcrData or not KEYSLINE[10] in OcrData:
        #         print(f" Line '{KEYSLINE[0]}' OR Line {KEYSLINE[10]} not in OCR {FilesTiff}")
        #         continue
        #     # use 'generator FOR LINE NAME '
        #     reslut=(next((item for item in missword if item["misword"] in OcrData['NAME']), None))
        #     if reslut != None :
        #         OcrData['NAME']=ReplaceMissword(OcrData['NAME'],reslut['misword'],reslut['rghword'],'misword')

        #     reslut=(next((item for item in missword if item["misword"] in OcrData['MOM']), None))
        #     if reslut != None :
        #         OcrData['MOM']=ReplaceMissword(OcrData['MOM'],reslut['misword'],reslut['rghword'],'misword')

        #     reslut=(next((item for item in missword if item["misword"] in OcrData['DAD']), None))
        #     if reslut != None :
        #         OcrData['DAD']=ReplaceMissword(OcrData['DAD'],reslut['misword'],reslut['rghword'],'misword')

        #     reslut=(next((item for item in missword if item["misword"] in OcrData['ADDR']), None))
        #     if reslut != None :
        #         OcrData['ADDR']=ReplaceMissword(OcrData['ADDR'],reslut['misword'],reslut['rghword'],'misword')

        #     # csv_dict_data.append(OcrData)
        #     filename =os.path.join(folderresult,os.path.basename(FilesTiff))    
        #     logproc=os.path.join(folderresult,os.path.basename(logproc))
        #     filePng =filename.replace('.tif','.png')
        #     Convertiftopng(FilesTiff,filePng)
        #     os.remove(FilesTiff)

        #     writhlogfile(logproc,f'{Nowstr_log()}\tOcr...Processing---:{FilesTiff}  ','a')
        #     writhlogfile(logproc,prettytxt(OcrData) ,'a')

        #     persondata=txtlinetostruct(locationg3,OcrData ,filePng,logproc)
        #     # dbdict_data.append(persondata)  use Mongo DB 
        #     qrystr={'idcard':persondata['idcard']}
        #     if finddocumentPerson(qrystr)!=None: # has IDCARD chage to Append & Update
        #         UpdatePersonAddr(persondata)
        #     else:
        #         x=InsertPersonDictOne(persondata)

        # InsertPersonDictMany(dbdict_data)    
