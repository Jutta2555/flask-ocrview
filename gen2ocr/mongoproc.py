import datetime

import pymongo
from pymongo.errors import ConnectionFailure, OperationFailure
from stlocrproject.gen2ocr.strfunc import KEYSDICT
# from stlocrproject.ocrfullpagestlv2 import Stldata

mgserver='mongodb://192.168.1.230:27017/'
dbname='addrocrtha'
collectionnamel='loctha'# collection of location thailand
collectionnamem='cmissthai' # collection of word thailand
collectionnamep='personscan3debug' # collection of Person OCR DATA 
myclient = pymongo.MongoClient(mgserver)
mydb = myclient[dbname]

def mongodb_close():
    print ("Connection Getting Closed")
    myclient.close()

def ConnectColdb(col):
    try:
        # The ismaster command is cheap and does not require auth.
        # myclient = pymongo.MongoClient(mgserver)
        # mydb = myclient[dbname]
        mycol = mydb[col]
        return mycol
    except ConnectionFailure:
        print("Server not available")
        return 

def locdb():
    mycol=ConnectColdb(collectionnamel)
    if mycol is not None:        
        # myquery = { "address": "Park Lane 38" }
        return  mycol.find().sort("misword")

def missworddb():
    mycol=ConnectColdb(collectionnamem)
    if mycol is not None:        
        # myquery = { "address": "Park Lane 38" }
        return  mycol.find()

def personscandb():
    mycol=ConnectColdb(collectionnamep)
    if mycol is not None:        
        # myquery = { "address": "Park Lane 38" }
        return  mycol.find()
def Updatepersonscandb(myquery,newvalues):
    mycol=ConnectColdb(collectionnamep)
    if mycol is not None:        
        try:
            mycol.update_one(myquery, newvalues)    
        except OperationFailure as e:           
            print(f"couldn't execute : {myquery,newvalues}.\n error as  {str(e)}") 
            return 




def UpdatemissPoint(myquery,newvalues):
    mycol=ConnectColdb(collectionnamem)
    if mycol is not None:        
        try:
            mycol.update_one(myquery, newvalues)    
        except OperationFailure as e:           
            print(f"couldn't execute : {myquery,newvalues}.\n error as  {str(e)}") 
            return 


#  INSERT Many LIST OF STLDATA DICT FORMAT
def InsertPersonDictMany(mylist):
    mycol=ConnectColdb(collectionnamep)
    try:
        x = mycol.insert_many(mylist)    
        return x
    except OperationFailure as e:           
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}") 
    return 


#  INSERT ONE STLDATA DICT FORMAT
def finddocumentPerson(stldata):
    mycol=ConnectColdb(collectionnamep)
    try:
        x = mycol.find_one(stldata)    
        return x
    except OperationFailure as e:           
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}") 
    return 

#  Update STLDATA DICT FORMAT & APPEND ARRY OF HISTORYADDRESS
def UpdatePersonAddr(mylist):
    mycol=ConnectColdb(collectionnamep)
    new_addr,strvalues='',''
    listdata=[]
    KEPTVAL=[1,3,4,5,6,7,8,13,18,20]
    # db.personscan.updateOne({'idcard':'-'},{ $set: { status: "x" },$push : { historyaddr: {name :'น.ส.ชิดชนก เทพอาชา',stlupdate:'26 เมษายน 2532่ในบนนี',sican : new Date()}}})
    # myquery={KEYSDICT[0]:mylist[KEYSDICT[0]]}
    # newvalues={"$set":{KEYSDICT[4]:mylist[KEYSDICT[4]] },"$push":{"historyaddr": {KEYSDICT[4]:mylist[KEYSDICT[4]],KEYSDICT[5]:mylist[KEYSDICT[5]],KEYSDICT[20]:datetime.datetime.utcnow()}}}
    # print()
    # print (myquery)
    # print()
    # print (newvalues)
    dumdic={}
    for k,v in mylist.items():
        if k=='idcard' :#idcard
            myquery = { k :v }
        else:
            kept= KEYSDICT.index(k)
            if kept in KEPTVAL :
                dumdic[k]=v

    # dumdic[KEYSDICT[20]]=datetime.datetime.utcnow()
    newvalues={"$set":dumdic ,"$push":{"historyaddr":dumdic}}

    try:
        x =mycol.update_one(myquery,newvalues)
        return x
    except OperationFailure as e:           
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}") 
    return 


#  INSERT ONE STLDATA DICT FORMAT
def InsertPersonDictOne(stldata):
    import datetime
    mycol=ConnectColdb(collectionnamep)
    KEPTVAL=[1,3,4,5,6,7,8,13,18]
    dumdic={}
    for k,v in stldata.items():
        kept= KEYSDICT.index(k)
        if kept in KEPTVAL :
            dumdic[k]=v
    dumdic[KEYSDICT[20]]=datetime.datetime.utcnow()
    listofdic=[dumdic]

    stldata['historyaddr']=listofdic

    try:
        x = mycol.insert_one(stldata)    
        return x
    except OperationFailure as e:           
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}") 
    return 
def main():
    print ('Run main in mongoproc.py')

    # mycol=ConnectColdb(collectionnamel)
    # if mycol is not None:        
    #     # myquery = { "address": "Park Lane 38" }
    #     x = mycol.find({PROVINCE:"กระบี่"}})    
    #     mylist=[]
    #     for x in mycol.find():
    #         mylist.append(x)
    #     print (len(mylist))
    #     print (mylist[0])
    #     print (mylist[0]['_id'])

if __name__ == '__main__' :
    main()

#               0           1           2           3       4           5       6
# KEYSDICT=['id_card','new_name','status_own','note_own','address','tumbol','amphur',
#          7        8           9       10          11      12          13          14
#     'province','zipcode','mother','id_mother','father','id_father','filescan','filetext',
#          15       16          17      18          19          20      21
#      'gender','nationality','dob','stlupdate','copydate','scandate','loaddate']

# key_list = list(dictionary)
# keys_of_interest = ['test2', 'test3']

# for key in keys_of_interest:
#     print('key: {}, index: {}'.format(key, key_list.index(key)))            
            # NAME x.keys().index("d")

# def update_tags(ref, new_tag):
#     coll.update({'ref': ref}, {'$push': {'tags': new_tag}})

# You can simply do
# 1) If you want to append single entry
# def update_tags(ref, new_tag):
#     coll.update({'ref': ref}, {'$push': {'tags': new_tag}})

# eg:
# {
#     "_id" : ObjectId("561c199e038e42b10956e3fc"),
#     "tags" : [ "tag1", "tag2", "tag3" ],
#     "ref" : "4780"
# }
# >> update_tags("4780", "tag4")
# {'updatedExisting': True, u'nModified': 1, u'ok': 1, u'n': 1}
# >> coll.find_one({"ref":"4780"})
# {
#     "_id" : ObjectId("561c199e038e42b10956e3fc"),
#     "tags" : [ "tag1", "tag2", "tag3" , "tag4" ],
#     "ref" : "4780"
# }

# print(mydb.list_collection_names())  
# collist = mydb.list_collection_names()
# if "customers" in collist:
#   print("The collection exists.")
            # if k== KEYSDICT[1] :
            #     strvalues=strvalues + f" '{KEYSDICT[1]}':'{mylist[KEYSDICT[1]]}', "
            # #note_own
            # if k== KEYSDICT[3]:
            #     strvalues=strvalues + ','+ KEYSDICT[3] +' : '+ mylist[KEYSDICT[3]]
            # #address
            # if k== KEYSDICT[4]:
            #     strvalues=strvalues + ','+ KEYSDICT[4] +' : '+ mylist[KEYSDICT[4]]
            #     new_addr=new_addr + ','+ KEYSDICT[4] +' : '+ mylist[KEYSDICT[4]]
            # if k== KEYSDICT[5]:
            #     strvalues=strvalues + ','+ KEYSDICT[5] +' : '+ mylist[KEYSDICT[5]]
            #     new_addr=new_addr + ','+ KEYSDICT[5] +' : '+ mylist[KEYSDICT[5]]
            # if k== KEYSDICT[6]:
            #     strvalues=strvalues + ','+ KEYSDICT[6] +' : '+ mylist[KEYSDICT[6]]
            #     new_addr=new_addr + ','+ KEYSDICT[6] +' : '+ mylist[KEYSDICT[6]]
            # if k== KEYSDICT[7]:
            #     strvalues=strvalues + ','+ KEYSDICT[7] +' : '+ mylist[KEYSDICT[7]]
            #     new_addr=new_addr + ','+ KEYSDICT[7] +' : '+ mylist[KEYSDICT[7]]
            # if k== KEYSDICT[8]:
            #     strvalues=strvalues + ','+ KEYSDICT[8] +' : '+ mylist[KEYSDICT[8]]
            #     new_addr=new_addr + ','+ KEYSDICT[8] +' : '+ mylist[KEYSDICT[8]]
            # # filescan
            # if k== KEYSDICT[13]:
            #     strvalues=strvalues + ','+ KEYSDICT[13] +' : '+ mylist[KEYSDICT[13]]
            #     new_addr=new_addr + ','+ KEYSDICT[13] +' : '+ mylist[KEYSDICT[13]]
            # if k== KEYSDICT[18]:
            #     strvalues=strvalues + ','+ KEYSDICT[18] +' : '+ mylist[KEYSDICT[18]] + ','+ KEYSDICT[19] +' : new Date()' 
            #     new_addr=new_addr + ','+ KEYSDICT[18] +' : '+ mylist[KEYSDICT[18]]  + ','+ KEYSDICT[19] +' : new Date()' 
# {'idcard': '1-6699-00131-27-7'},
