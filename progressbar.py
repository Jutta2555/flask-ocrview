from flask import Flask, render_template, request
import os
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def data_page():

    if request.method == 'POST':
        filesDict = request.files.to_dict()
        uploadData = request.files['media']
        data_file_name = uploadData.filename
        uploadData.save(os.path.join(
            app.root_path, 'uploads', data_file_name))

    return render_template("upload.html")


if __name__ == '__main__':
    app.run(debug=True)
