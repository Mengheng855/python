from flask import Flask,render_template,redirect,request,flash,session
import pymysql
import secrets
from pymysql.cursors import DictCursor
from functools import wraps
app=Flask(__name__)
app.secret_key = '1a2b3c4d5e6f7890abcdef1234567890'
def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='db_flask_auth'
    )
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'danger')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated
@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin/dashboard.html')
@app.route('/')
def index():
    return render_template('user/user.html')
@app.route('/register',methods=['POST','GET'])

def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        conn=get_db()
        cursor=conn.cursor()
        sql="INSERT INTO user (name,email,password) VALUES (%s,%s,%s)"
        cursor.execute(sql,(name,email,password))
        conn.commit()
        return redirect('/login')
    return render_template('auth/register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        if not email or not password:
            flash('All fields are required.', 'danger')
            return redirect('/login')
        conn=get_db()
        cursor=conn.cursor(DictCursor)
        cursor.execute("SELECT * FROM user WHERE email=%s",(email))
        user=cursor.fetchone()
        if user and user['password']==password:
            session['user_id']=user['id']
            session['is_admin']=bool(user['is_admin'])
            if session['is_admin']==0:
                flash(f"Welcome back, {user['name']}!", 'success')
                return redirect('/')
            else:
                flash(f"Welcome back, {user['name']}!", 'success')
                return redirect('/admin')
    return render_template('auth/login.html')
if __name__=="__main__":
    app.run(debug=True)