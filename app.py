from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_pymongo import PyMongo
import json
from pymongo.errors import ConnectionFailure, OperationFailure

app = Flask(__name__)
app.secret_key = 'secret'
app.config["MONGO_URI"] = "mongodb://192.168.1.230:27017/addrocrtha"
mongo = PyMongo(app) #addrocrtha.personscan4
conllection = mongo.db.personscan5

totalfile=conllection.count_documents( {} )
totalcheked=conllection.count_documents( {"checked":1})
fileperpage=10
print('totalfile :',totalfile)


#  INSERT ONE STLDATA DICT FORMAT
def finddocumentcmissthai(stldata):
    try:
        x = mongo.db.cmissthai.find_one(stldata)    
        return x
    except OperationFailure as e:           
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}") 
    return 

#  INSERT ONE STLDATA DICT FORMAT
def Insertmissword(stldata):
    import datetime
    try:
        x = mongo.db.cmissthai.insert_one(stldata)    
        return x
    except OperationFailure as e:           
        print(f"couldn't execute insert_many mylist.\n error as  {str(e)}") 
    return 
                
@app.route('/')
def index():
    listpage=totalfile//fileperpage    
    page=0
    return render_template('base.html',ocrdata=[],page=int(page),listpage=listpage,totalcheked=totalcheked,totalfile=totalfile)

@app.route('/page/<int:page>')
def page(page):
    """Update a author."""
    # print(page)
    listpage=totalfile//fileperpage    
    skipfile=fileperpage*int(page)
    totalcheked=conllection.count_documents( {"checked":1})
    ocrdata=conllection.find().limit(fileperpage).skip(skipfile)
    return render_template('base.html',ocrdata=ocrdata,page=int(page),listpage=listpage,totalcheked=totalcheked,totalfile=totalfile)

    
@app.route('/toggleUpdate', methods=['POST'])
def toggleUpdate():
    dumdict=request.form.to_dict()
    myquery={'index_file':int(dumdict['index_file'])}
    dumdict=dict(request.form)
    if dumdict['checked']=='1' :
        conllection.update_one(myquery,{'$set':{'checked':0}})
        return json.dumps('Cancle');
        
    dumdict['checked']=1
    dumdict.pop('index_file')
    newvalues = { "$set": dumdict }
    conllection.update_one(myquery, newvalues)        
    return json.dumps('Update');


@app.route('/addmissword', methods=['POST'])
def addmissword():
    dumdict=request.form.to_dict()
    
    if finddocumentcmissthai({'misword':dumdict['misword']})==None: # has IDCARD chage to Append & Update
        dumdict['fcount']=1
        x=Insertmissword(dumdict)
    return json.dumps('add');
# addrocrtha.cmissthai{
#     "_id": {
#         "$oid": "617b81aee51f35f234e233ce"
#     },
#     "misword": "สูทิน",
#     "rghword": "สุทิน",
#     "fcount": 1
# }

if __name__ == '__main__':
    app.run(debug=True)