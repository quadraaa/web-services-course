from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file, flash
import os
import sys
app = Flask(__name__)
import numpy as np
import pandas as pd
from joblib import load
clf = load('./knn.joblib')


@app.route('/')
def hello_world():
    print('Printed smth')
    return 'Hello, my very best friend!!!!!'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    username = float(username) * float(username)
    return 'User %s' % username

def mean(numbers):
    return float(sum(numbers))/max(len(numbers), 1)

@app.route('/avg/<nums>')
def avg(nums):
    nums = nums.split(',')
    nums = [float(x) for x in nums]
    print(nums)
    nums_mean = mean(nums)  
    return str(nums_mean)

@app.route('/iris/<param>')
def iris(param):

    param = param.split(',')
    param = [float(x) for x in param]
    param = np.array(param).reshape(1, -1)
    
    preds = clf .predict(param)
    
    return str(preds)

@app.route('/show_image')
def show_image():
    return '<img src="/static/setosa.jpg" alt="setosa">'

@app.route('/badrequest400')
def bad_request():
    return abort(400)


@app.route('/iris_post', methods=['POST'])
def add_message():
    try:
        content = request.get_json()
        print(content)

        param = content['flower'].split(',')
        param = [float(x) for x in param]
        param = np.array(param).reshape(1, -1)
    
        preds = clf.predict(param)
    
        response = {}
        response['flower'] = str(preds)

    except:
         return redirect(url_for('bad_request'))

    return jsonify(response)






from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField(validators=[DataRequired()])

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
       
        	


        f = form.file.data
        df = pd.read_csv(f, header = None)
        print(df.head())
        predictions = clf.predict(df)
        print(predictions)
        df['predictions'] = predictions
        filename = secure_filename(f.filename)
        filename = 'scored_' + filename
        print(filename)
      
        df.to_csv(filename, index = False, header=None)

        return send_file(filename, mimetype='text/csv', attachment_filename = filename, as_attachment = True)


    return render_template('submit.html', form=form)



import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename('uploaded_' + file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(filepath)
            return 'file uploaded'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''







