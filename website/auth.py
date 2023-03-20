from flask import Blueprint, render_template, request, flash, redirect, url_for,session,Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import mysql.connector
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="mydb"
    
)

mycursor = mydb.cursor()

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password, ))
        user = mycursor.fetchone()
        if user:
            session['logged_in'] = True
            session['username']= user[0]
            session['email']=user[1]
            session['first_name']=user[2]
            session['last_name']=user[3]
            session['ic_number']=user[4]
            session['mobile_number']=user[5]
            session['address']=user[6]
            session['password']=user[7]
            user_authenticated = True
            return redirect('/menu' )
        else:
            flash('Incorrect username or password, try again.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)    
    session.pop('email', None)    
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('ic_number', None)
    session.pop('mobile_number', None)
    session.pop('address', None)
    session.pop('password', None)
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    print(session)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        ic_number = request.form.get('icNumber')
        mobile_number = request.form.get('mobileNumber')
        address = request.form.get('address')
        registrationCode = request.form.get('registrationCode')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        mycursor.execute('SELECT * FROM admin WHERE username = '"'"+username+"'")
        user = mycursor.fetchone()
        if user is None:
            if password1 != password2:
                flash("Confirm password doesn't match New password .", category='error')
            elif len(username) < 3 or len(username) > 15:
                flash("Username must be between 3 and 15 characters long.", category='error')
            elif len(email) < 4 or len(email) > 40:
                flash("Email must be between 4 and 40 characters long.", category='error')
            elif len(first_name) < 2 or len(first_name) > 40:
                flash("First name must be between 4 and 40 characters long.", category='error')
            elif len(last_name) < 2 or len(last_name) > 40 :
                flash("Last name must be between 4 and 40 characters long.", category='error')
            elif len(ic_number) < 10 or len(ic_number) > 12 :
                flash("Ic number must be between 10 and 12 digits long.", category='error')
            elif not ic_number.isdigit():
                flash("Ic number must be numeric.", category='error')
            elif len(mobile_number) < 7 or len(mobile_number) > 12:
                flash("Mobile number must be between 7 and 12 digits long.", category='error')
            elif not mobile_number.isdigit():
                flash("Mobile number must be numeric.", category='error')
            elif len(password1) < 6 or len(password1) > 25:
                flash("Password must be between 6 and 25 characters long.", category='error')
            elif len(address) < 6 or len(address) > 97:
                flash("Address must be between 6 and 80 characters long.", category='error')
            else:

                ''' 
                query = "INSERT INTO admin (username, email, first_name, last_name, ic_number, mobile_number, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                admin = (username, email, first_name, last_name, ic_number, mobile_number, address, password1)
                mycursor.execute(query, admin)
                '''
                query = "insert into admin values ('"+ username+ "','"+ email+ "','"+ first_name+ "', '"+ last_name+ "',"+ ic_number+ ","+ mobile_number+ ",'"+ address+ "','"+ password1+ "')"
                mycursor.execute(query)
                mydb.commit()
                
                flash('Account created!', category='success')
                session['logged_in'] = True
                session['username']= username
                session['email']=email
                session['first_name']=first_name
                session['last_name']=last_name
                session['ic_number']=ic_number
                session['mobile_number']=mobile_number
                session['address']=address
                session['password']=password1


            

        else : 
            flash('Username already exists.', category='error')
    return render_template("sign_up.html", user=current_user)


@auth.route('/profile',methods=['GET','POST'])
def user_profile():
    if request.method =='POST':
        current_username = session['username']
        username=request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        ic_number = request.form.get('icNumber')
        mobile_number = request.form.get('mobileNumber')
        address = request.form.get('address')
        password1 = request.form.get('password1')
        mycursor.execute('SELECT * FROM admin WHERE username = '"'"+username+"'")
        user = mycursor.fetchone()
        print(email)
        if user is None or username == session['username']:
            if username is "" or username == session['username']:
                username = session['username']
            if email is "" or email == session['email']:
                email = session['email']

            if first_name is "" or first_name ==session['first_name']:
                first_name = session['first_name']

            if last_name is  "" or last_name ==  session['last_name']:
                last_name = session['last_name']

            if ic_number is "" or ic_number == session['ic_number']:
                ic_number = str(session['ic_number'])

            if mobile_number is "" or mobile_number == session['mobile_number'] :
                mobile_number = str(session['mobile_number'])

            if address is "" or address == session['address']:
                address = session['address']

            if password1 is "" or password1 == session['password'] :
                password1 = session['password']

            if  len(username) < 3 or len(username) > 15 :
                flash("Username must be between 3 and 15 characters long.", category='error')
                return render_template("profile.html", user=current_user)
            if len(email) < 4 or len(email) > 40:
                flash("Email must be between 4 and 40 characters long.", category='error')
                return render_template("profile.html", user=current_user)
            if len(first_name) < 2 or len(first_name) > 40:
                flash("First name must be between 4 and 40 characters long.", category='error')
                return render_template("profile.html", user=current_user)
            if len(last_name) < 2 or len(last_name) > 40 :
                flash("Last name must be between 4 and 40 characters long.", category='error')
                return render_template("profile.html", user=current_user)
            if len(ic_number) < 10 or len(ic_number) > 12 :
                flash("Ic number must be between 10 and 12 digits long.", category='error')
                return render_template("profile.html", user=current_user)
            if not ic_number.isdigit():
                flash("Ic number must be numeric.", category='error')
                return render_template("profile.html", user=current_user)
            if len(mobile_number) < 7 or len(mobile_number) > 12:
                flash("Mobile number must be between 7 and 12 digits long.", category='error')
                return render_template("profile.html", user=current_user)
            if not mobile_number.isdigit():
                flash("Mobile number must be numeric.", category='error')
                return render_template("profile.html", user=current_user)
            if len(password1) < 6 or len(password1) > 25:
                flash("Password must be between 6 and 25 characters long.", category='error')
                return render_template("profile.html", user=current_user)
            if len(address) < 6 or len(address) > 97:
                flash("Address must be between 6 and 80 characters long.", category='error')
                return render_template("profile.html", user=current_user)

            mycursor.execute("UPDATE admin SET username ='"+username+"',email = '"+email+"',first_name ='"+first_name+"', last_name='"+last_name+"',ic_number="+ic_number+",mobile_number="+mobile_number+",address='"+address+"',password='"+password1+"' WHERE username = '"+current_username+"'" )
            mydb.commit()
            flash('Account updated!', category='success')
            session['logged_in'] = True
            session['username']= username
            session['email']=email
            session['first_name']=first_name
            session['last_name']=last_name
            session['ic_number']=ic_number
            session['mobile_number']=mobile_number
            session['address']=address
            session['password']=password1
            return render_template("profile.html", user=current_user)
        else : 
            flash('Username already exists.', category='error')

    return render_template("profile.html", user=current_user)

