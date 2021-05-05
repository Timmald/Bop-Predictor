import os
import tempfile

from flask import Flask, render_template, request, url_for, flash
import sqlite3

from werkzeug.utils import redirect, secure_filename

from AI.Song import Song
from AI.fileAnalyzer import main
from AI.AI import main as AI



app = Flask(__name__)
app.config['SECRET_KEY']='dfsdfsdfsdfsgsdfsdvsdf'
app.config['UPLOAD_FOLDER'] = '/Users/nathanwolf/Documents/coding/PycharmProjects/bop predictor with flask/audio files'
ALLOWED_EXTENSIONS=['.wav']
def get_db_connection():
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=('GET','POST'))
def index():
    if request.method=='POST':
        if request.method == 'POST':
            # check if the post request has the file part
            print('received')
            print(str(request.files))
            file = request.files['wavFile']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                print('no file')
                flash('No selected file')
                return redirect(request.url)
            print('GOOD')
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        name=file.filename
        bass,vocal,originality=main(name)
        feat= ',' in request.form['artistNames']
        instrument=request.form['mainInstrument']
        #get all the values

        conn=get_db_connection()
        exists=len(conn.execute('SELECT * FROM songs WHERE name=?',(name,)).fetchall())>0
        print(f'exitsts={exists}')
        if not exists:
            conn.execute("INSERT INTO songs (name,bass,feat,vocal,instrument,originality) VALUES (?,?,?,?,?,?)",(name,bass,feat,vocal,instrument,originality))#params are added as second param
            conn.commit()
            print('inserted!')
        conn.close()

        songObj=Song(name,bass,feat,vocal,instrument,originality)
        isBop=AI(songObj)
        if isBop:
            predictionString='It IS a bop!'
        else:
            predictionString='It IS NOT a bop!'
        return render_template('index.html',prediction=predictionString,feedback=url_for('feedback'))
    return render_template('index.html',prediction="Please upload a file to get your prediction!",feedback='#')
@app.route('/feedback',methods=('GET','POST'))
def feedback():
    if request.method=='POST':
        wasBop=request.form['isBop']=='It was a bop'
        conn=get_db_connection()
        mostrecentID=len(conn.execute('SELECT * FROM songs').fetchall())
        conn.execute('UPDATE songs SET isBop = ? WHERE id = ?',(wasBop,mostrecentID))
        conn.commit()
        print(tuple(conn.execute('SELECT * FROM songs WHERE id=?',(mostrecentID,)).fetchone()))
        conn.close()
        return redirect(url_for('index'))
    return render_template('feedback.html')

