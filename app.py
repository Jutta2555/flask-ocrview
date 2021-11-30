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
    print(id)
    print(page)
    if request.method == "POST":
        dumdict=dict(request.form)
        dumdict['checked']=1
        dumdict.pop('index_file')

        newvalues = { "$set": dumdict }
        myquery={'index_file':int(request.form['index_file'])}
        # print(myquery)
        # print(newvalues)
        res=mongo.db.personscan4.update_one(myquery, newvalues)
        # print(res)
           
    listpage=totalfile//fileperpage    
    skipfile=fileperpage*int(page)
    ocrdata=mongo.db.personscan4.find().limit(fileperpage).skip(skipfile)
    return render_template('base.html',ocrdata=ocrdata,page=int(page),listpage=listpage)


# @app.route("/<int:id>,<int:page>/update", methods=("GET", "POST"))
# def update(id,page):
#     """Update a author."""
#     print(id)
#     print(page)
#     if request.method == "POST":
#         dumdict=dict(request.form)
#         dumdict['checked']=1
#         dumdict.pop('index_file')

#         newvalues = { "$set": dumdict }
#         myquery={'index_file':int(request.form['index_file'])}
#         print(myquery)
#         print(newvalues)
#         res=mongo.db.personscan4.update_one(myquery, newvalues)
#         print(res)
#         redirect(url_for('page',page=page))
#     listpage=totalfile//fileperpage    
#     skipfile=fileperpage*int(page)
#     ocrdata=mongo.db.personscan4.find().limit(fileperpage).skip(skipfile)

#     return  render_template('base.html',ocrdata=ocrdata,page=int(page),listpage=listpage)

    
if __name__ == '__main__':
    app.run(debug=True)