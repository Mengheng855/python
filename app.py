from flask import Flask , render_template , redirect ,request,session,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from pymysql.cursors import DictCursor
import os
import pymysql
app=Flask(__name__)
app.secret_key="wsetrjhujlakreugysd23456"
def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='db_flask_project'
    )
app.config['UPLOADE_FOLDER']='static/productImage'
@app.route('/')
def index():
    products = [
        {
            'badge': 'New',
            'badge_type': '',
            'image_url': 'https://i.pinimg.com/1200x/aa/5e/b5/aa5eb5a473f10d73bbc621d16e24c5a6.jpg',
            'category': 'Smartphones',
            'name': 'ProMax Ultra 5G',
            'stars': ['fill', 'fill', 'fill', 'fill', 'half'],
            'rating_count': 128,
            'price_old': '$1,299',
            'price_current': '$999'
        },
        {
            'badge': None,
            'badge_type': '',
            'image_url': None,
            'placeholder_class': 'laptop',
            'category': 'Laptops',
            'name': 'UltraBook Pro 15"',
            'stars': ['fill', 'fill', 'fill', 'fill', 'fill'],
            'rating_count': 256,
            'price_old': None,
            'price_current': '$1,799'
        },
        {
            'badge': 'Sale',
            'badge_type': 'sale',
            'image_url': None,
            'placeholder_class': 'headphones',
            'category': 'Audio',
            'name': 'SoundMax Pro ANC',
            'stars': ['fill', 'fill', 'fill', 'fill', ''],
            'rating_count': 89,
            'price_old': '$449',
            'price_current': '$349'
        },
        {
            'badge': None,
            'badge_type': '',
            'image_url': None,
            'placeholder_class': 'watch',
            'category': 'Wearables',
            'name': 'FitWatch Elite',
            'stars': ['fill', 'fill', 'fill', 'fill', 'half'],
            'rating_count': 174,
            'price_old': None,
            'price_current': '$299'
        }
    ]
    return render_template('user/index.html', products=products)
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        conn=get_db()
        cursor=conn.cursor(DictCursor)
        cursor.execute("SELECT * FROM user WHERE email=%s",(email))
        user=cursor.fetchone()
        if user:
            if check_password_hash(user['password'],password):
                session['is_admin']=user['is_admin']
                session['username']=user['username']
                session['user_id']=user['user_id']
                session['email']=user['email']
                if user['is_admin']==0:
                    return redirect('/')
                elif user['is_admin']==1:
                    return redirect('/admin')
                else:
                    return redirect('/login')
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    return render_template('auth/login.html')
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=="POST":
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        if password==confirm_password:
            password=generate_password_hash(password)
            conn=get_db()
            cursor=conn.cursor()
            cursor.execute("INSERT INTO user (username,email,password) VALUES (%s,%s,%s)",(username,email,password))
            conn.commit()
            return redirect('/login')
        else:
            return redirect('/register')
    return render_template('auth/register.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route('/admin')

def admin():
    if session.get('is_admin')!=1:
        return redirect('/')
    return render_template('admin/dashboard.html', total_products='247', active_products='189', low_stock_products='23', out_of_stock='8')
@app.route('/admin/user')
def user():
    if session.get('is_admin')!=1:
        return redirect('/')
    conn=get_db()
    cursor=conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM user")
    users=cursor.fetchall()
    return render_template('admin/user.html', users=users)
@app.route('/admin/product')
def product():
    if session.get('is_admin')!=1:
        return redirect('/')
    if request.method=="POST":
        name=request.form['productName']
        price=request.form['price']
        status=request.form['status']
        discount=request.form['discount']
        stock=request.form['stock']
        file=request.files['file']
        if file:
            filepath=os.path.join(app.config['UPLOADE_FOLDER'],file.filename)
            file_url=request.host_url+url_for('static',filename='uploads/'+file.filename)
            file.save(filepath)

    return render_template('admin/product.html')

@app.route('/admin/category',methods=['POST','GET'])
def category():
    if session.get('is_admin')!=1:
        return redirect('/')
    conn=get_db()
    cursor=conn.cursor()
    if request.method=="POST":
        cate_name=request.form['cate_name']
        user_id=session.get('user_id')
        cursor.execute("INSERT INTO category (name,user_id) VALUES (%s,%s)",(cate_name,user_id))
        conn.commit()
    
    cursor.execute("""
        SELECT c.cate_id, c.name, c.created_at, c.updated_at, a.username
        FROM category c
        LEFT JOIN user a ON c.user_id = a.user_id
    """)
    cate=cursor.fetchall()
    return render_template('admin/category.html',cate=cate)
if __name__=='__main__':
    app.run(debug=True)



