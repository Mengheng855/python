from flask import Flask,jsonify,request
import pymysql,os
from pymysql.cursors import DictCursor
from werkzeug.utils import secure_filename
app=Flask(__name__)
UPLOAD_FOLDER='static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='db_flask_api_crud'
    )
def response(message,status,data):
    return jsonify({
        'message':message,
        'status':status,
        'data':data
    })
@app.route('/',methods=['GET'])
def index():
   conn=get_db()
   cursor=conn.cursor(DictCursor)
   cursor.execute("SELECT * FROM student")
   data=cursor.fetchall()
   if data:
       return response('success',200,data)
   else:
       return response('unsuccess',500,None)  
@app.route('/addStudent',methods=['POST'])
def addStudent():
    name=request.form['username']
    sex=request.form['sex']
    profile=request.files['profile']
    fileName=secure_filename(profile.filename)
    filepath=os.path.join(app.config['UPLOAD_FOLDER'],fileName)
    profile.save(filepath)
    url=request.host_url+"static/uploads/"+fileName
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute('INSERT INTO student (username,sex,profile) VALUES (%s,%s,%s)',(name,sex,url))
    conn.commit()
    return jsonify({
        'message':'cerated',
        'status':201
    })
@app.route('/deleteStudent/<int:id>',methods=['POST'])
def deleteStudent(id):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute('DELETE FROM student WHERE id=%s',(id))
    conn.commit()
    return jsonify({
        'message':'success',
        'status':200
    })    
@app.route('/editStudent/<int:id>',methods=['PATCH'])
def editStudent(id):
    name=request.form['username']
    sex=request.form['sex']
    profile=request.files['profile']
    fileName=secure_filename(profile.filename)
    filepath=os.path.join(app.config['UPLOAD_FOLDER'],fileName)
    profile.save(filepath)
    url=request.host_url+"static/uploads/"+fileName
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute('UPDATE student SET username=%s, sex=%s, profile=%s',(name,sex,url))
    conn.commit()
    return jsonify({
        'message':'success',
        'status':200
    })
@app.route('/student/<int:id>')
def student(id):
    conn=get_db()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM student WHERE id=%s',(id))
    data=cursor.fetchone()
    if data:
       return response('success',200,data)
    else:
        return response('unsuccess',500,None)  
if __name__=="__main__":
    app.run(debug=True)
