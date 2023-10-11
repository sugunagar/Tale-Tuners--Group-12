from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Configure MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='3033',
    database='storytel'
)

# Set a secret key for session management
app.secret_key = 'storytel'

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastaname = request.form['lastname']
        password = request.form['password']
        cpassword=request.form['cpassword']
        pnnumber=request.form['pnnumber']
        email=request.form['email']
        
        if password == cpassword:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (firstname,lastname,email,pnnumber,password) VALUES (%s, %s,%s,%s,%s)", (firstname,lastaname,email,pnnumber,password))
            db.commit()
            cursor.close()
            flash('1')
            
        else:
            flash('2')
            
        return render_template('./signup.html')
    return render_template('./signup.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE email = '{username}' AND password ='{password}'")
        user = cursor.fetchall()
        #print(user[0][1])
        cursor.close()  # Close the cursor after fetching the result
        cato_list=[["Adventure","adventure.jpeg"],["Fantasy","fantasy.jpeg"],["Horror","fiction.jpeg"],["Historical","historical.jpeg"],["Fiction","horror.jpeg"]]
        
        if user:
            session['firstname'] = user[0][1]
            session['lastname'] = user[0][2]
            session['userid'] = user[0][0]
            session['email']=user[0][3]
            receiver_email=session['email']
            user_name=session['firstname']+session['lastname']
            #send_mail(receiver_email,user_name)
            flash('Login successful!')
            return render_template('home.html',username=user_name,catlit=cato_list)
        else:
            flash('wrong')
    return render_template('login.html')
@app.route('/category', methods=['GET', 'POST'])
def category_selection():
    if request.method=='POST':
        selected_categories = request.form.getlist('gener')

        print(selected_categories)
        return render_template('userPage.html',sc=selected_categories)


# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def send_mail(receiver_email,user_name):
    sender_email = 'tejeshvenna@gail.com' 
    receiver_email = f'{receiver_email}' 
    subject = 'Login Detected'
    message = f'''
<pre style="font-family: Arial, Helvetica, sans-serif;text-align: justify;">
Hi {user_name},

Login Detected

</pre>
'''


    smtp_server = 'smtp.gmail.com'
    smtp_port = 587 
    smtp_username = 'saikrishnabandi25@gmail.com'  
    smtp_password = 'ejypitgoawfizqnf'  


    email_body = MIMEText(message, 'html')

    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject

    email_message.attach(email_body)


    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, email_message.as_string())
        server.quit()
        return (f'{receiver_email} Email sent successfully!')

    except Exception as e:
        return (f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
