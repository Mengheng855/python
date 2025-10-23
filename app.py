from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
import os
import pymysql

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'  # Store uploads in static/uploads for serving as static files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='db_flask_crud',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['POST', 'GET'])
def index():
    connection = get_db()
    cur = connection.cursor()
    
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        file = request.files.get('profile')  # Get the uploaded file
        profile_url = 'https://i.pinimg.com/736x/48/14/9a/48149a338a2e318825c44845c3a50b40.jpg'  # Default URL

        # Validate and save the uploaded file
        if file and file.filename:
            # Validate file extension
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(f"Saving file to: {filepath}")  # Debug: Check file path
                file.save(filepath)
                profile_url = url_for('static', filename=f'uploads/{filename}', _external=True)
                print(f"Generated profile URL: {profile_url}")  # Debug: Check generated URL
            else:
                cur.close()
                connection.close()
                return render_template('index.html', error="Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.")

        try:
            cur.execute("INSERT INTO user (name, email, profile) VALUES (%s, %s, %s)", (name, email, profile_url))
            connection.commit()
            print(f"Inserted user: {name}, {email}, {profile_url}")  # Debug: Confirm insertion
        except Exception as e:
            connection.rollback()
            print(f"Error: {e}")
            return render_template('index.html', error="Failed to add user")
        finally:
            cur.close()
            connection.close()
        
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    cur.close()
    connection.close()
    
    return render_template('index.html', users=users)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    connection = get_db()
    cur = connection.cursor()
    try:
        cur.execute("DELETE FROM user WHERE id=%s", (id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        connection.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    connection = get_db()
    cur = connection.cursor()
    
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        file = request.files.get('profile')
        cur.execute("SELECT profile FROM user WHERE id=%s", (id,))
        current_user = cur.fetchone()
        profile_url = current_user['profile']

        if file and file.filename:
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                profile_url = url_for('static', filename=f'uploads/{filename}', _external=True)
            else:
                cur.close()
                connection.close()
                return render_template('edit.html', error="Invalid file type.", user={'id': id, 'name': name, 'email': email})

        try:
            cur.execute("UPDATE user SET name=%s, email=%s, profile=%s WHERE id=%s", 
                        (name, email, profile_url, id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error: {e}")
        finally:
            cur.close()
            connection.close()
        return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM user WHERE id=%s", (id,))
    user = cur.fetchone()
    cur.close()
    connection.close()
    return render_template('edit.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)