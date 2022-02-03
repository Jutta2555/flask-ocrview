MONTHTHAI=['มกราคม','กมภาพนธ','มนาคม','เมษายน','พฤษภาคม','มถนายน','กรกฎาคม','สงหาคม','กนยายน','ตลาคม','พฤศจกายน','ธนวาคม']
# NUMTHAI='๐๑๒๓๔๕๖๗๘๙'
SARATHAI=" ี ุ ื ๊ ๋ ู ิ ้ ็แเ ัะ ์ไใ ึโ ่ ํา"
SARATHAILINE= " ี ุ ื ๊ ๋ ู ิ ้ ็ ั ์ ึ ่ ํ"
# SPECAILCHAR="<>«»="
# NATIONAL_THCHAR='ไทยอินเดียจีน'
# GENDERTHCHAR=['ชาย','ซาย','หญิง']
# STATUSHOME=['เจ้าบ้าน','ผู้อาศัย','หัวหน้าครอบครัว']
# DIGITINLINE='[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
PROVINCETHA=['กระบี่','กรุงเทพมหานคร','กาญจนบุรี','กาฬสินธุ์','กำแพงเพชร','ขอนแก่น','จันทบุรี','ฉะเชิงเทรา','ชลบุรี','ชัยนาท','ชัยภูมิ','ชุมพร','เชียงราย','เชียงใหม่','ตรัง','ตราด','ตาก','นครนายก','นครปฐม','นครพนม','นครราชสีมา','นครศรีธรรมราช','นครสวรรค์','นนทบุรี','นราธิวาส','น่าน','บึงกาฬ','บุรีรัมย์','ปทุมธานี','ประจวบคีรีขันธ์','ปราจีนบุรี','ปัตตานี','พระนครศรีอยุธยา','พะเยา','พังงา','พัทลุง','พิจิตร','พิษณุโลก','เพชรบุรี','เพชรบูรณ์','แพร่','ภูเก็ต','มหาสารคาม','มุกดาหาร','แม่ฮ่องสอน','ยโสธร','ยะลา','ร้อยเอ็ด','ระนอง','ระยอง','ราชบุรี','ลพบุรี','ลำปาง','ลำพูน','เลย','ศรีสะเกษ','สกลนคร','สงขลา','สตูล','สมุทรปราการ','สมุทรสงคราม','สมุทรสาคร','สระแก้ว','สระบุรี','สิงห์บุรี','สุโขทัย','สุพรรณบุรี','สุราษฎร์ธานี','สุรินทร์','หนองคาย','หนองบัวลำภู','อ่างทอง','อำนาจเจริญ','อุดรธานี','อุตรดิตถ์','อุทัยธานี','อุบลราชธานี']
DISTINLINE=['จ.','ต.','อ.','เขต','แขวง','กรุงเทพมหานคร']
def stringchrTha(s,z):
    x = " " # ช=ซ
    y = " "
    mychraum = s.maketrans(x,y,z)
    findstr=s.translate(mychraum)
    return findstr


PROVINCETHAWITHOUTSARA=list(stringchrTha(pv,SARATHAILINE)   for pv in PROVINCETHA )
# print(PROVINCETHAWITHOUTSARA)
# print ('กรงเทพมหานคร')
stchk='งเทพมหานคร'
# stchk='ง3333'

# _Nones = [high.append(x) if is_condition_true() else low.append(x) for x in sequences
# when iterated over, `even_gen` will generate 0.. 2.. 4.. ... 98
even_gen = (i for i in range(100) if i%2 == 0)
x=[pv for pv in PROVINCETHAWITHOUTSARA  if stchk in pv  ] # ช=ซ

# x=(True if stchk in pv else False for pv in PROVINCETHAWITHOUTSARA ,True ) # ช=ซ
    # global Linedata    
    # global KEYSLINE
    # global DISTINLINE#=['จ.','ต.','อ.','เขต','แขวง','กรุงเทพมหานคร']
    # global MONTHTHAI#=['มกราคม','กมภาพนธ','มนาคม','เมษายน','พฤษภาคม','มถนายน','กรกฎาคม','สงหาคม','กนยายน','ตลาคม','พฤศจกายน','ธนวาคม']
    # global NUMTHAI#='๐๑๒๓๔๕๖๗๘๙'
    # global SARATHAI#=" ี ุ ื ๊ ๋ ู ิ ้ ็แเ ัะ ์ไใ ึโ ่ ํา"
    # global SPECAILCHAR#="<>«»="
    # global NATIONAL_THCHAR#='ไทยอินเดียจีน'
    # global GENDERTHCHAR#=['ชาย','ซาย','หญิง']
    # global STATUSHOME#=['เจ้าบ้าน','ผู้อาศัย','หัวหน้าครอบครัว']
    # global DIGITINLINE
# print(type(x))
# print(list(x))
# print(len(x))
OcrData={}
OcrData['ADDR']='417 หมู่ 8 ต.สันทราย อะ.เมืองเชียงราย จ.เชียงราย'

linetextlaw=OcrData['ADDR']
DistCount=0


listDistCount= list( 1 for d in DISTINLINE if d in linetextlaw )
# DistCount=listDistCount.count(1)
DistCount=len(listDistCount)

print ('GenerotorAlgo {} '.format(DistCount))

newDict={w:len(w) for w in linetextlaw.split()}
sort_by_value = dict(sorted(newDict.items() , reverse=True , key=lambda item: item[1])) #

MonthMatch=(True for k in sort_by_value.keys() if stringchrTha(k,SARATHAILINE) in MONTHTHAI)


# Nested list comprehensions.
# This creates a 3x4 "matrix" (list of lists) of zeros.
# print([[0 for col in range(4)] for row in range(3)])
# [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

print('MonthMatch= {} '.format(MonthMatch))
# print('old Algo {} '.format(sort_by_value))


# print('new Algo {} '.format(newDict))
# print('new Algo {} '.format(sort_by_value))
# listkey=list(sort_by_value.values())
# listvalues=list(sort_by_value.values())[0]
# print (listvalues)
# print(listvalues[0])