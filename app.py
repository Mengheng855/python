from flask import Flask , render_template , redirect ,request,session,url_for
from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash,check_password_hash
from pymysql.cursors import DictCursor
import os
import pymysql
app=Flask(__name__)
app.secret_key="wsetrjhujlakreugysd23456"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mengheng.mh855@gmail.com'  
app.config['MAIL_PASSWORD'] = 'gtvs fxmr vimk phhx'     
app.config['MAIL_DEFAULT_SENDER'] = 'mengheng.mh855@gmail.com'
mail = Mail(app)
def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='db_flask_project'
    )
app.config['UPLOADE_FOLDER']='static/productImage'
@app.route('/subscribe',methods=['POST'])
def subscribe():
    email = request.form.get('email', '').strip()
    if not email:
        return redirect(request.referrer or '/')

    print(f"Subscribe route called with email: {email}")
    try:
        print(f"Attempting to subscribe email: {email}")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM newsletter WHERE email = %s", (email,))
        existing = cursor.fetchone()

        if existing:
            print(f"Email {email} already exists")
            return redirect(request.referrer + '?error=already_subscribed' if request.referrer else '/?error=already_subscribed')

        print("Sending welcome email...")
        msg = Message(
            subject='WELCOME TO NEXUS',
            recipients=[email],
            body='Thank you for subscribing to NEXUS! You will receive exclusive offers, product launches, and tech insights delivered to your inbox.'
        )
        try:
            mail.send(msg)
            print("Email sent successfully")
        except Exception as mail_error:
            print(f"Failed to send email: {mail_error}")
            raise

        print("Saving to database...")
        cursor.execute("INSERT INTO newsletter (email) VALUES (%s)", (email,))
        conn.commit()
        print("Database saved successfully")

        return redirect(request.referrer + '?success=subscribed' if request.referrer else '/?success=subscribed')

    except Exception as e:
        print(f"Error subscribing user: {e}")
        import traceback
        traceback.print_exc()
        return redirect(request.referrer + '?error=subscription_failed' if request.referrer else '/?error=subscription_failed')
@app.route('/')
def index():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("""
        SELECT p.pro_id, p.pro_name, p.price, p.discount, p.total, p.stock,  p.image,
                c.name as category_name
        FROM product p
        INNER JOIN user u ON p.user_id = u.user_id
        INNER JOIN category c ON p.cate_id = c.cate_id
    """)
    products=cursor.fetchall()
    cursor.execute('SELECT * FROM category')
    category=cursor.fetchall()
    return render_template('user/index.html', products=products,category=category)
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
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM user')
    total_user=cursor.fetchone()[0]
    return render_template('admin/user.html', users=users,total_user=total_user)
@app.route('/admin/product',methods=['POST','GET'])
def product():
    if session.get('is_admin')!=1:
        return redirect('/')
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT cate_id, name FROM category")
    cate=cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM product")
    total_product = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM product WHERE status=1")
    active_product = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM product WHERE stock<10")
    low_product = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM product WHERE stock=0")
    out_product = cursor.fetchone()[0]
    cursor.execute('SELECT status FROM product')
    status=cursor.fetchall()
    cursor.execute("""
        SELECT p.pro_id, p.pro_name, p.price, p.discount, p.total, p.stock, p.status, p.image,
               p.created_at, p.updated_at, u.username, c.name as category_name
        FROM product p
        INNER JOIN user u ON p.user_id = u.user_id
        INNER JOIN category c ON p.cate_id = c.cate_id
    """)
    if request.method=="POST":
        name=request.form['productName']
        price=float(request.form['price'])
        status=request.form['status']
        discount=float(request.form['discount']) if request.form['discount'] else 0 
        stock=request.form['stock']
        total=float(price-((price*discount)/100))
        cate_id=request.form['category']
        user_id=session.get('user_id')
        file=request.files['file']
        if file:
            filepath=os.path.join(app.config['UPLOADE_FOLDER'],file.filename)
            file_url=request.host_url+url_for('static',filename='productImage/'+file.filename)
            file.save(filepath)
        cursor.execute("""
            INSERT INTO product (pro_name,price,discount,total,stock,status,image,user_id,cate_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (name,price,discount,total,stock,status,file_url,user_id,cate_id))
        conn.commit()
        return redirect('/admin/product')
    cursor.execute("""
        SELECT p.pro_id, p.pro_name, p.price, p.discount, p.total, p.stock, p.status, p.image, 
               p.created_at, p.updated_at, u.username, c.name as category_name
        FROM product p
        INNER JOIN user u ON p.user_id = u.user_id
        INNER JOIN category c ON p.cate_id = c.cate_id
    """)
    product=cursor.fetchall()
    return render_template('admin/product.html',cate=cate,product=product,total_product=total_product,active_product=active_product,low_product=low_product,out_product=out_product,status=status)
@app.route('/admin/deleteProduct/<int:id>')
def deleteProduct(id):
    if session.get('is_admin')!=1:
        return redirect('/')
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM product WHERE pro_id=%s",(id))
    conn.commit()
    return redirect('/admin/product')
@app.route('/admin/editProduct/<int:id>',methods=['POST'])
def editProduct(id):
    conn=get_db()
    cursor=conn.cursor()
    if request.method=='POST':
        name=request.form['productName']
        price=float(request.form['price'])
        status=request.form['status']
        discount=float(request.form['discount']) if request.form['discount'] else 0 
        stock=request.form['stock']
        total=float(price-((price*discount)/100))
        cate_id=request.form['category']
        user_id=session.get('user_id')
        file_url = request.form.get('image', '') 
        if request.files:
            file = request.files['file']
            if file.filename:
                file.save(os.path.join(app.config['UPLOADE_FOLDER'], file.filename))
                file_url = request.host_url + url_for('static', filename='productImage/' + file.filename)
    
        
        cursor.execute("""
            UPDATE product SET pro_name=%s, price=%s, discount=%s, total=%s, stock=%s, status=%s, image=%s,user_id=%s, cate_id=%s WHERE pro_id=%s
            """,(name,price,discount,total,stock,status,file_url,user_id,cate_id,id))
        conn.commit()
        return redirect('/admin/product')
@app.route('/admin/category',methods=['POST','GET'])
def category():
    if session.get('is_admin')!=1:
        return redirect('/')
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM category')
    total_cate=cursor.fetchone()[0]
    # cursor.execute('SELECT COUNT(*) FROM category WHERE st')
    if request.method=="POST":
        cate_name=request.form['cate_name']
        user_id=session.get('user_id')
        cursor.execute("INSERT INTO category (name,user_id) VALUES (%s,%s)",(cate_name,user_id))
        conn.commit()
    
    cursor.execute("""
        SELECT c.cate_id, c.name, c.created_at, c.updated_at, a.username
        FROM category c
        INNER JOIN user a ON c.user_id = a.user_id
    """)
    cate=cursor.fetchall()
    return render_template('admin/category.html',cate=cate,total_cate=total_cate)
@app.route('/admin/deleteCategory/<int:id>')
def deleteCategory(id):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM category WHERE cate_id=%s",(id))
    conn.commit()
    return redirect('/admin/category')
@app.route('/admin/editCategory/<int:id>',methods=['POST'])
def editCategory(id):
    conn=get_db()
    cursor=conn.cursor()
    if request.method=="POST":
        cate_name=request.form['cate_name']
        user_id=session.get('user_id')
        cursor.execute('UPDATE category SET name=%s, user_id=%s WHERE cate_id=%s',(cate_name,user_id,id))
        conn.commit()
        return redirect('/admin/category')
if __name__=='__main__':
    app.run(debug=True)



