from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)
app.secret_key = 'secret'
app.config["MONGO_URI"] = "mongodb://192.168.1.230:27017/addrocrtha"
mongo = PyMongo(app) #addrocrtha.personscan4

# totalfile=mongo.db.personscan4.find().count()
totalfile=mongo.db.personscan4.count_documents( {} )
fileperpage=6
print('totalfile :',totalfile)

class OCRUser:  
    def Update(self):      
        return jsonify({ "error": "Invalid login credentials" }), 401
                
@app.route('/')
def index():
    listpage=totalfile//fileperpage    
    page=0
    skipfile=fileperpage*int(page)
    ocrdata=mongo.db.personscan4.find().limit(fileperpage).skip(skipfile)
    return render_template('base.html',ocrdata=[],page=int(page),listpage=listpage)

@app.route('/page/<int:page>', methods=("GET","POST"))
def page(page):
    """Update a author."""
    print(page)
    if request.method == "POST":
        myquery={'index_file':int(request.form['index_file'])}
        dumdict=dict(request.form)
        if dumdict['checked']=='1' :
            # print('checked')
            # print(dumdict)
            mongo.db.personscan4.update_one(myquery,{'$set':{'checked':0}})
            return redirect(url_for('page', page=page))
        
        dumdict['checked']=1
        dumdict.pop('index_file')
        newvalues = { "$set": dumdict }
        res=mongo.db.personscan4.update_one(myquery, newvalues)        
        return redirect(url_for('page', page=page))

    listpage=totalfile//fileperpage    
    skipfile=fileperpage*int(page)
    ocrdata=mongo.db.personscan4.find().limit(fileperpage).skip(skipfile)
    return render_template('base.html',ocrdata=ocrdata,page=int(page),listpage=listpage)

@app.route('/OCRuser/Update', methods=['POST'])
def login():
  return OCRUser().Update()
    
if __name__ == '__main__':
    app.run(debug=True)