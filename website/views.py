from flask import Blueprint, render_template, request, redirect, url_for,flash, jsonify,session,Response
from flask_login import login_required, current_user
import plotly
import plotly.express as px
import pandas as pd
import json
import csv
import cv2
import numpy as np

import mysql.connector
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from flask import Blueprint, current_app
from PIL import Image
from ultralytics import YOLO
import urllib.request
import random
import string
import subprocess
import shutil

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="mydb"
)

mycursor = mydb.cursor()
views = Blueprint('views', __name__)
camera = cv2.VideoCapture(0)
                # Perform face detection and cropping using YOLO
model_path = '/Users/yunka/Desktop/New folder (5)/train-yolov8-custom-dataset-step-by-step-guide-master/runs/detect/train22/weights/last.pt'  # Replace with your YOLO model path
model = YOLO(model_path)

threshold = 0.0000
margin = 5


def generate_frames():

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():
 
    return render_template("home.html")

@views.route('/menu', methods=['GET', 'POST'])
#@login_required
def menu():
 
    return render_template("menu.html")






@views.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@views.route('/manage_employees', methods=['GET', 'POST'])
def manage_employees():
    rows= []
    query = "select * from employee"
    mycursor.execute(query)
    rows = mycursor.fetchall()

    if request.method == 'POST':
        employee_id = request.form.get('employee_id') 
        button_value = request.form.get('add_employee')
        button_delete = request.form.get('action')
        
        if button_delete != None : 
            mycursor.execute('SELECT * FROM employee WHERE employee_id = '"'"+button_delete+"'")
            employee = mycursor.fetchone()
            print(button_delete)
            if employee:
                name = employee[1]
                print(name)
                folder_path = 'C:/Users/yunka/Desktop/New folder (5)/train-yolov8-custom-dataset-step-by-step-guide-master/local_env/faces/'+name
                print(folder_path)

                if os.path.exists(folder_path):
                    try:
                        shutil.rmtree(folder_path)
                        mycursor.execute("DELETE FROM employee WHERE employee_id = %s", (button_delete,))
                        mydb.commit()
                        print(f"Folder '{folder_path}' and its contents have been deleted.")
                    except Exception as e:
                        print(f"Error deleting folder '{folder_path}': {e}")
                else:
                        mycursor.execute("DELETE FROM employee WHERE employee_id = %s", (button_delete,))
                        mydb.commit()
            return redirect('/manage_employees')



        if button_value == 'submit':
            
            return redirect(url_for('views.sign_up_employee'))  
        

        if  employee_id :
            
            mycursor.execute('SELECT * FROM employee WHERE employee_id = '"'"+employee_id+"'")
            employee = mycursor.fetchone()
            if employee:
                session['employee_id']= employee[0]
                session["employee_name"] = employee[1]
                session["employee_email"] = employee[2]
                session["employee_ic"] = employee[3]
                session["employee_mobile"] = employee[4]
                session["employee_transportation_expense"] = employee[5]
                session["employee_distance_to_work"] = employee[6]
                session["employee_daily_work_load"] = employee[7]
                session["employee_bmi"] = employee[8]
                session["employee_education"]=employee[9]
                session["employee_pets"]= employee[10]
                session["employee_address"] = employee[11]
                session["employee_work_position"]= employee[12]
                session["employee_children"]= employee[13]


            #employee_id = request.form.get('employee_id')

            return redirect(url_for('views.edit_employee',id = employee_id))
            
    return render_template('manage_employees.html', table_data=rows)

 
@views.route('/edit_employee', methods=['GET', 'POST'])
def edit_employee():
    if request.method == 'POST':

        employee_id=request.form.get('employee_id')
        employee_name = request.form.get('employee_name')
        employee_email=request.form.get('employee_email')
        employee_ic = request.form.get('employee_ic')
        employee_mobile = request.form.get('employee_mobile')
        employee_transportation_expense = request.form.get('employee_transportation_expense')
        employee_distance_to_work = request.form.get('employee_distance_to_work')
        employee_daily_work_load = request.form.get('employee_daily_work_load')
        employee_bmi = request.form.get('employee_bmi')
        employee_education = request.form.get('employee_education')
        employee_pets = request.form.get('employee_pets')
        employee_address = request.form.get('employee_address')
        employee_work_position = request.form.get('employee_work_position')
        employee_children = request.form.get('employee_children')

        mycursor.execute('SELECT * FROM employee WHERE employee_id ='"'"+employee_id+"'")
        employee = mycursor.fetchone()
        #employee_id= session['employee_id']
        if employee is None:
            if employee_id is "" :
                employee_id = session["employee_id"]
            if employee_name is "" :
                employee_name = session["employee_name"] 
            if employee_email is "" :
                employee_email = session["employee_email"] 
            if employee_ic is "" :
                employee_ic = session["employee_ic"]
            if employee_mobile is "" :
                employee_mobile= session["employee_mobile"] 
            if employee_transportation_expense is "" :
                employee_transportation_expense= session["employee_transportation_expense"] 
            if employee_distance_to_work is "" :
                employee_distance_to_work=  session["employee_distance_to_work"]
            if employee_daily_work_load is "" :
                employee_daily_work_load= session["employee_daily_work_load"] 
            if employee_bmi is "" :
                employee_bmi= session["employee_bmi"] 
            if employee_education is "" :
                employee_education= session["employee_education"]
            if employee_pets is "" :
                employee_pets= session["employee_pets"]
            if employee_address is "" :
                employee_address=session["employee_address"]
            if employee_work_position is "" :
                employee_work_position= session["employee_work_position"]
            if employee_children is "" :
                employee_children= session["employee_children"]

            if len(str(employee_id)) < 0 or len(str(employee_id)) > 3:
                flash("Employee ID must be between 1 and 3 numbers long.", category='error')
            elif not str(employee_id).isdigit():
                flash("Employee ID must be numeric.", category='error')     
            elif len(employee_email) < 4 or len(employee_email) > 60:
                flash("Employee email must be between 4 and 60 characters long.", category='error')
            elif len(employee_name) < 2 or len(employee_name) > 60:
                flash("Employee name must be between 2 and 60 characters long.", category='error')
            elif str(employee_name).isdigit():
                flash("Employee name must be characters only.", category='error')
            elif len(str(employee_ic)) < 10 or len(str(employee_ic)) > 13:
                flash("Employee IC number must be between 10 and 13 digits long.", category='error')
            elif not str(employee_ic).isdigit():
                flash("Employee IC number must be numeric.", category='error')
            elif len(str(employee_mobile)) < 7 or len(str(employee_mobile)) > 12:
                flash("Employee mobile number must be between 7 and 12 digits long.", category='error')
            elif not str(employee_mobile).isdigit():
                flash("Employee mobile number must be numeric.", category='error')
            elif len(str(employee_transportation_expense)) > 10:
                flash("Transportation expense must be a number with up to 10 digits.", category='error')
            elif not str(employee_transportation_expense).isdigit():
                flash("Transportation expense must be numeric.", category='error')                
            elif len(str(employee_distance_to_work)) > 10:
                flash("Distance to work must be a number with up to 10 digits.", category='error')
            elif not str(employee_distance_to_work).isdigit():
                flash("Distance to work must be numeric.", category='error')   
            elif len(str(employee_daily_work_load)) > 7:
                flash("Daily work load average must be a number with up to 7 digits.", category='error')
            elif not str(employee_daily_work_load).isdigit():
                flash("Daily work load average must be numeric.", category='error')   
            elif len(str(employee_bmi)) > 4:
                flash("BMI must be a number with up to 4 digits.", category='error')
            elif not str(employee_bmi).isdigit():
                flash("BMI must be numeric.", category='error')   
            elif len(str(employee_education)) > 1:
                flash("Education level must be a number with up to 1 digit.", category='error')
            elif not str(employee_education).isdigit():
                flash("Education level must be numeric.", category='error')  
            elif len(str(employee_pets)) > 2:
                flash("Number of pets must be a number with up to 2 digits.", category='error')
            elif not str(employee_pets).isdigit():
                flash("Number of pets must be numeric.", category='error')  
            elif len(employee_address) < 6 or len(employee_address) > 99:
                flash("Address must be between 6 and 99 characters long.", category='error')
            elif len(employee_work_position) < 1 or len(employee_work_position) > 50:
                flash("Work position must be between 1 and 50 characters long.", category='error')
            elif len(str(employee_children)) < 0 or len(str(employee_children)) > 2:
                flash("Number of children must be between 0 and 2 digits long.", category='error')
            elif not str(employee_children).isdigit():
                flash("Number of children must be numeric.", category='error')
            else:
                #query = "update employee set employee_id = "+ employee_id+ ",employee_name = '"+ employee_name+ "',employee_email ='"+ employee_email+ "',employee_ic = '"+ employee_ic+ "',employee_mobile ='"+ employee_mobile+ "',transportation_exp = "+ employee_transportation_expense+ ",distance_to_work ="+ employee_distance_to_work+ ",daily_work_load_average ="+ employee_daily_work_load+ ", bmi = "+ employee_bmi+ ",education ="+ employee_education+ ",pets ="+ employee_pets+ ",address ='"+ employee_address+ "',work_position ='"+ employee_work_position+ "',children = "+ employee_children+ ")"
                #query = "UPDATE employee SET employee_id = " + str(employee_id) + ", employee_name = '" + employee_name + "', employee_email = '" + employee_email + "', employee_ic = '" + str(employee_ic) + "', employee_mobile = '" + str(employee_mobile) + "', transportation_exp = " + str(employee_transportation_expense) + ", distance_to_work = " + str(employee_distance_to_work) + ", daily_work_load_average = " + str(employee_daily_work_load) + ", bmi = " + str(employee_bmi) + ", education = " + str(employee_education) + ", pets = " + str(employee_pets) + ", address = '" + employee_address + "', work_position = '" + employee_work_position + "', children = " + str(employee_children) +"where employee_id = "+str(employee_id)
                
                query = "UPDATE employee SET employee_id = " + str(employee_id) + ", employee_name = '" + employee_name + "', employee_email = '" + employee_email + "', employee_ic = '" + str(employee_ic) + "', employee_mobile = '" + str(employee_mobile) + "', transportation_exp = " + str(employee_transportation_expense) + ", distance_to_work = " + str(employee_distance_to_work) + ", daily_work_load_average = " + str(employee_daily_work_load) + ", bmi = " + str(employee_bmi) + ", education = " + str(employee_education) + ", pets = " + str(employee_pets) + ", address = '" + employee_address + "', work_position = '" + employee_work_position + "', children = " + str(employee_children) +" WHERE employee_id = "+str(session["employee_id"])

                print(query)
                mycursor.execute(query)
                mydb.commit()
                #mycursor.execute("")
                
                flash('Employee information updated !', category='success')


                return redirect('/manage_employees')
                #return redirect(url_for('views.home'))
        
        else : 
            flash('This ID already exists.', category='error')
            #flash('Employee already exists.', category='error')
        # Extract form data for modification
        #new_name = request.form.get('name')
        #new_salary = request.form.get('salary')

        # Update the employee record in the database
        #query = "UPDATE employee SET name = %s, salary = %s WHERE id = %s"
        #mycursor.execute(query, (new_name, new_salary, employee_id))
        # Commit the changes to the database
        #mycursor.commit()
        #mycursor.close()
        #return redirect(url_for('views.manage_employees'))
    
    # Fetch the employee record to pre-populate the edit form
    #query = "SELECT * FROM employee WHERE id = %s"
    #mycursor.execute(query, (employee_id,))
    #employee = mycursor.fetchone()
    #mycursor.close()

    return render_template('edit_employee.html')


@views.route('/api/data', methods=['GET'])
def get_data():
    dataset = []

    # Read the CSV file
    with open('/Users/yunka/Desktop/New folder (3)/fyp11/data_analysis/dataset/data.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dataset.append(dict(row))

    # Return the dataset as a JSON response
    return jsonify(dataset=dataset)


@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    csv_file_path = '/Users/yunka/Desktop/New folder (3)/fyp11/data_analysis/dataset/data.csv'

    # Read the CSV file into a DataFrame
    dataset = pd.read_csv(csv_file_path)
    # Count the occurrences of 0 and 1 in the Attend column
    attend_counts = dataset['Attend'].value_counts()
    # Create the pie chart
    labels = ['0', '1']
    values = [attend_counts.get(0, 0), attend_counts.get(1, 0)]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # Update the layout
    fig.update_layout(
    title="Attend Counts",
    annotations=[dict(text='Attend Counts', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph5JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    first_select = request.form.getlist('firstSelect')
    second_select = request.form.getlist('secondSelect')
    print(first_select)
    print(second_select)
    if request.method == 'POST':

        selected_options = request.form.get('selectBar')
        display_sentence = "You seddddlected: " 
        print("Selected Options:", selected_options)
        first_select = request.form.getlist('firstSelect')
        second_select = request.form.getlist('secondSelect')
        selected_date = request.form.getlist('selectedDate')
        selected_checkboxes = request.form.getlist('checkbox')

        #print(len(selected_checkboxes))
        if len(selected_checkboxes) != 2:
            error_message = "Please select exactly two checkboxes."
            return render_template('dashboard.html', error_message=error_message)
        else:
            success_message = "Selected checkboxes: {}".format(selected_checkboxes)
            print(len(selected_checkboxes))

        # Graph four
        df = pd.read_csv('/Users/yunka/Desktop/New folder (3)/fyp1/dataset/Absenteeism.csv')
        # Provide the path to your CSV file

        if len(selected_checkboxes) == 2:
            if len(selected_checkboxes[0]) != 0 and len(selected_checkboxes[1]) != 0:
                fig4 = px.bar(df, x=selected_checkboxes[0], y=selected_checkboxes[1], title="Absenteeism11111")
                graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            
        else:
            fig4 = px.bar(df, x="ID", y="Absenteeism Time in Hours", title="Absenteeism")
            graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template("dashboard.html", graph4JSON=graph4JSON,graph5JSON=graph5JSON)
    
    #return render_template("dashboard.html",display_sentence="display_sentence")
    return render_template("dashboard.html",graph5JSON=graph5JSON)


@views.route('/dashboardpage_1', methods=['GET', 'POST'])
def dashboardpage_1():

    csv_file_path = '/Users/yunka/Desktop/New folder (3)/fyp11/data_analysis/dataset/data.csv'

    # Read the CSV file into a DataFrame
    dataset = pd.read_csv(csv_file_path)
    # Count the occurrences of 0 and 1 in the Attend column
    attend_counts = dataset['Attend'].value_counts()
    # Create the pie chart
    labels = ['0', '1']
    values = [attend_counts.get(0, 0), attend_counts.get(1, 0)]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # Update the layout
    fig.update_layout(
    title="Attend Counts",
    annotations=[dict(text='Attend Counts', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph5JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    first_select = request.form.getlist('firstSelect')
    second_select = request.form.getlist('secondSelect')
    print(first_select)
    print(second_select)
    if request.method == 'POST':

        selected_options = request.form.get('selectBar')
        display_sentence = "You seddddlected: " 
        print("Selected Options:", selected_options)
        first_select = request.form.getlist('firstSelect')
        second_select = request.form.getlist('secondSelect')
        selected_date = request.form.getlist('selectedDate')
        selected_checkboxes = request.form.getlist('checkbox')

        #print(len(selected_checkboxes))
        if len(selected_checkboxes) != 2:
            error_message = "Please select exactly two checkboxes."
            return render_template('dashboard.html', error_message=error_message)
        else:
            success_message = "Selected checkboxes: {}".format(selected_checkboxes)
            print(len(selected_checkboxes))

        # Graph four
        df = pd.read_csv('/Users/yunka/Desktop/New folder (3)/fyp1/dataset/Absenteeism.csv')
        # Provide the path to your CSV file

        if len(selected_checkboxes) == 2:
            if len(selected_checkboxes[0]) != 0 and len(selected_checkboxes[1]) != 0:
                fig4 = px.bar(df, x=selected_checkboxes[0], y=selected_checkboxes[1], title="Absenteeism11111")
                graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

        else:
            fig4 = px.bar(df, x="ID", y="Absenteeism Time in Hours", title="Absenteeism")
            graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template("dashboardpage_1.html", graph4JSON=graph4JSON,graph5JSON=graph5JSON)
    
    #return render_template("dashboard.html",display_sentence="display_sentence")
    return render_template("dashboardpage_1.html",graph5JSON=graph5JSON)




@views.route('/dashboardpage_2', methods=['GET', 'POST'])
def dashboardpage_2():

    csv_file_path = '/Users/yunka/Desktop/New folder (3)/fyp11/data_analysis/dataset/data.csv'

    # Read the CSV file into a DataFrame
    dataset = pd.read_csv(csv_file_path)
    # Count the occurrences of 0 and 1 in the Attend column
    attend_counts = dataset['Attend'].value_counts()
    # Create the pie chart
    labels = ['0', '1']
    values = [attend_counts.get(0, 0), attend_counts.get(1, 0)]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # Update the layout
    fig.update_layout(
    title="Attend Counts",
    annotations=[dict(text='Attend Counts', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph5JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    first_select = request.form.getlist('firstSelect')
    second_select = request.form.getlist('secondSelect')
    print(first_select)
    print(second_select)
    if request.method == 'POST':

        selected_options = request.form.get('selectBar')
        display_sentence = "You seddddlected: " 
        print("Selected Options:", selected_options)
        first_select = request.form.getlist('firstSelect')
        second_select = request.form.getlist('secondSelect')
        selected_date = request.form.getlist('selectedDate')
        selected_checkboxes = request.form.getlist('checkbox')

        #print(len(selected_checkboxes))
        if len(selected_checkboxes) != 2:
            error_message = "Please select exactly two checkboxes."
            return render_template('dashboard.html', error_message=error_message)
        else:
            success_message = "Selected checkboxes: {}".format(selected_checkboxes)
            print(len(selected_checkboxes))


        # Graph four
        df = pd.read_csv('/Users/yunka/Desktop/New folder (3)/fyp1/dataset/Absenteeism.csv')
        # Provide the path to your CSV file


        if len(selected_checkboxes) == 2:
            if len(selected_checkboxes[0]) != 0 and len(selected_checkboxes[1]) != 0:
                fig4 = px.bar(df, x=selected_checkboxes[0], y=selected_checkboxes[1], title="Absenteeism11111")
                graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            

        else:
            fig4 = px.bar(df, x="ID", y="Absenteeism Time in Hours", title="Absenteeism")
            graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


        

        return render_template("dashboardpage_2.html", graph4JSON=graph4JSON,graph5JSON=graph5JSON)
    
    #return render_template("dashboard.html",display_sentence="display_sentence")
    return render_template("dashboardpage_2.html",graph5JSON=graph5JSON)


@views.route('/dashboardpage_3', methods=['GET', 'POST'])
def dashboardpage_3():


    csv_file_path = '/Users/yunka/Desktop/New folder (3)/fyp11/data_analysis/dataset/data.csv'

    # Read the CSV file into a DataFrame
    dataset = pd.read_csv(csv_file_path)
    # Count the occurrences of 0 and 1 in the Attend column
    attend_counts = dataset['Attend'].value_counts()
    # Create the pie chart
    labels = ['0', '1']
    values = [attend_counts.get(0, 0), attend_counts.get(1, 0)]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # Update the layout
    fig.update_layout(
    title="Attend Counts",
    annotations=[dict(text='Attend Counts', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph5JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    first_select = request.form.getlist('firstSelect')
    second_select = request.form.getlist('secondSelect')
    print(first_select)
    print(second_select)
    if request.method == 'POST':

        selected_options = request.form.get('selectBar')
        display_sentence = "You seddddlected: " 
        print("Selected Options:", selected_options)
        first_select = request.form.getlist('firstSelect')
        second_select = request.form.getlist('secondSelect')
        selected_date = request.form.getlist('selectedDate')
        selected_checkboxes = request.form.getlist('checkbox')

        #print(len(selected_checkboxes))
        if len(selected_checkboxes) != 2:
            error_message = "Please select exactly two checkboxes."
            return render_template('dashboard.html', error_message=error_message)
        else:
            success_message = "Selected checkboxes: {}".format(selected_checkboxes)
            print(len(selected_checkboxes))

        # Graph four
        df = pd.read_csv('/Users/yunka/Desktop/New folder (3)/fyp1/dataset/Absenteeism.csv')
        # Provide the path to your CSV file


        if len(selected_checkboxes) == 2:
            if len(selected_checkboxes[0]) != 0 and len(selected_checkboxes[1]) != 0:
                fig4 = px.bar(df, x=selected_checkboxes[0], y=selected_checkboxes[1], title="Absenteeism11111")
                graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            

        else:
            fig4 = px.bar(df, x="ID", y="Absenteeism Time in Hours", title="Absenteeism")
            graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


        

        return render_template("dashboardpage_3.html", graph4JSON=graph4JSON,graph5JSON=graph5JSON)
    
    #return render_template("dashboard.html",display_sentence="display_sentence")
    return render_template("dashboardpage_3.html",graph5JSON=graph5JSON)


@views.route('/dashboardpage_4', methods=['GET', 'POST'])
def dashboardpage_4():

    csv_file_path = '/Users/yunka/Desktop/New folder (3)/fyp11/data_analysis/dataset/data.csv'
    # Read the CSV file into a DataFrame
    dataset = pd.read_csv(csv_file_path)
    # Count the occurrences of 0 and 1 in the Attend column
    attend_counts = dataset['Attend'].value_counts()
    # Create the pie chart
    labels = ['0', '1']
    values = [attend_counts.get(0, 0), attend_counts.get(1, 0)]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # Update the layout
    fig.update_layout(
    title="Attend Counts",
    annotations=[dict(text='Attend Counts', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    graph5JSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    first_select = request.form.getlist('firstSelect')
    second_select = request.form.getlist('secondSelect')
    print(first_select)
    print(second_select)
    if request.method == 'POST':

        selected_options = request.form.get('selectBar')
        display_sentence = "You seddddlected: " 
        print("Selected Options:", selected_options)
        first_select = request.form.getlist('firstSelect')
        second_select = request.form.getlist('secondSelect')
        selected_date = request.form.getlist('selectedDate')
        selected_checkboxes = request.form.getlist('checkbox')

        #print(len(selected_checkboxes))
        if len(selected_checkboxes) != 2:
            error_message = "Please select exactly two checkboxes."
            return render_template('dashboard.html', error_message=error_message)
        else:
            success_message = "Selected checkboxes: {}".format(selected_checkboxes)
            print(len(selected_checkboxes))

        # Graph four
        df = pd.read_csv('/Users/yunka/Desktop/New folder (3)/fyp1/dataset/Absenteeism.csv')
        # Provide the path to your CSV file

        if len(selected_checkboxes) == 2:
            if len(selected_checkboxes[0]) != 0 and len(selected_checkboxes[1]) != 0:
                fig4 = px.bar(df, x=selected_checkboxes[0], y=selected_checkboxes[1], title="Absenteeism11111")
                graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            

        else:
            fig4 = px.bar(df, x="ID", y="Absenteeism Time in Hours", title="Absenteeism")
            graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


        

        return render_template("dashboardpage_4.html", graph4JSON=graph4JSON,graph5JSON=graph5JSON)
    
    #return render_template("dashboard.html",display_sentence="display_sentence")
    return render_template("dashboardpage_4.html",graph5JSON=graph5JSON)






@views.route('/sign_up_employee',methods=['GET','POST'])
def sign_up_employee():
    if request.method =='POST':
        employee_id=request.form.get('employee_id')
        employee_name = request.form.get('employee_name')
        employee_email=request.form.get('employee_email')
        employee_ic = request.form.get('employee_ic')
        employee_mobile = request.form.get('employee_mobile')
        employee_transportation_expense = request.form.get('employee_transportation_expense')
        employee_distance_to_work = request.form.get('employee_distance_to_work')
        employee_daily_work_load = request.form.get('employee_daily_work_load')
        employee_bmi = request.form.get('employee_bmi')
        employee_education = request.form.get('employee_education')
        employee_pets = request.form.get('employee_pets')
        employee_address = request.form.get('employee_address')
        employee_work_position = request.form.get('employee_work_position')
        employee_children = request.form.get('employee_children')

        mycursor.execute('SELECT * FROM employee WHERE employee_id = %s', (employee_id,))
        user = mycursor.fetchone()
        if user is None:
            if len(employee_id) < 0 or len(employee_id) > 3:
                flash("Employee ID must be between 1 and 3 numbers long.", category='error')
            elif not str(employee_id).isdigit():
                flash("Employee ID must be numeric.", category='error')     
            elif len(employee_email) < 4 or len(employee_email) > 60:
                flash("Employee email must be between 4 and 60 characters long.", category='error')
            elif len(employee_name) < 2 or len(employee_name) > 60:
                flash("Employee name must be between 2 and 60 characters long.", category='error')
            elif str(employee_name).isdigit():
                flash("Employee name must be characters only.", category='error')
            elif len(str(employee_ic)) < 10 or len(str(employee_ic)) > 13:
                flash("Employee IC number must be between 10 and 13 digits long.", category='error')
            elif not str(employee_ic).isdigit():
                flash("Employee IC number must be numeric.", category='error')
            elif len(str(employee_mobile)) < 7 or len(str(employee_mobile)) > 12:
                flash("Employee mobile number must be between 7 and 12 digits long.", category='error')
            elif not str(employee_mobile).isdigit():
                flash("Employee mobile number must be numeric.", category='error')
            elif len(str(employee_transportation_expense)) > 10:
                flash("Transportation expense must be a number with up to 10 digits.", category='error')
            elif not str(employee_transportation_expense).isdigit():
                flash("Transportation expense must be numeric.", category='error')                
            elif len(str(employee_distance_to_work)) > 10:
                flash("Distance to work must be a number with up to 10 digits.", category='error')
            elif not str(employee_distance_to_work).isdigit():
                flash("Distance to work must be numeric.", category='error')   
            elif len(str(employee_daily_work_load)) > 7:
                flash("Daily work load average must be a number with up to 7 digits.", category='error')
            elif not str(employee_daily_work_load).isdigit():
                flash("Daily work load average must be numeric.", category='error')   
            elif len(str(employee_bmi)) > 4:
                flash("BMI must be a number with up to 4 digits.", category='error')
            elif not str(employee_bmi).isdigit():
                flash("BMI must be numeric.", category='error')   
            elif len(str(employee_education)) > 1:
                flash("Education level must be a number with up to 1 digit.", category='error')
            elif not str(employee_education).isdigit():
                flash("Education level must be numeric.", category='error')  
            elif len(str(employee_pets)) > 2:
                flash("Number of pets must be a number with up to 2 digits.", category='error')
            elif not str(employee_pets).isdigit():
                flash("Number of pets must be numeric.", category='error')  
            elif len(employee_address) < 6 or len(employee_address) > 99:
                flash("Address must be between 6 and 99 characters long.", category='error')
            elif len(employee_work_position) < 1 or len(employee_work_position) > 50:
                flash("Work position must be between 1 and 50 characters long.", category='error')
            elif len(str(employee_children)) < 0 or len(str(employee_children)) > 2:
                flash("Number of children must be between 0 and 2 digits long.", category='error')
            elif not str(employee_children).isdigit():
                flash("Number of children must be numeric.", category='error')
            else:
                #query = "INSERT INTO employee (employee_id,employee_name,employee_email,employee_ic,employee_mobile,transportation_exp,distance_to_work,daily_work_load_average,bmi,education,pets,address,work_position,children) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                #employee_data = (employee_id, employee_name, employee_email, employee_ic, employee_mobile, employee_transportation_expense,employee_distance_to_work , employee_daily_work_load, employee_bmi, employee_education, employee_pets, employee_address, employee_work_position, employee_children)
                query = "insert into employee values ("+ employee_id+ ",'"+ employee_name+ "','"+ employee_email+ "','"+ employee_ic+ "','"+ employee_mobile+ "', "+ employee_transportation_expense+ ","+ employee_distance_to_work+ ","+ employee_daily_work_load+ ","+ employee_bmi+ ","+ employee_education+ ","+ employee_pets+ ",'"+ employee_address+ "','"+ employee_work_position+ "',"+ employee_children+ ")"
                print(query)
                mycursor.execute(query)
                
                #mycursor.execute("")
                mydb.commit()
                flash('Account created!', category='success')
                parent_folder_path = 'C:/Users/yunka/Desktop/New folder (3)/fyp11/faces_recognition/data/data_faces_from_camera'
                folder_name = 'person_'+employee_name
                folder_path = os.path.join(parent_folder_path, folder_name)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print("Folder created successfully.")
                else:
                    print("Folder already exists.")
        
            
               
        else : 
            flash('Username already exists.', category='error')


    return render_template("sign_up_employee.html", user=current_user)


class UploadFileForm(FlaskForm):
    files = FileField("Files", validators=[InputRequired()], render_kw={"multiple": True})
    submit = SubmitField("Upload Files")

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_random_filename(length=10, extension=""):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    filename = f"{random_string}.{extension}"
    return filename

@views.route('/face_registration', methods=['GET', 'POST'])
def face_registration():
    #UPLOAD_FOLDER = '\\Users\\yunka\\Desktop\\New folder (3)\\fyp11\\faces_recognition\\data\\data_faces_from_camera\\person_'
    UPLOAD_FOLDER = '\\Users\\yunka\\Desktop\\New folder (5)\\train-yolov8-custom-dataset-step-by-step-guide-master\\local_env\\faces\\'
    mycursor.execute('SELECT employee_name FROM employee')
    results = mycursor.fetchall()
    employee_names = [result[0] for result in results]
    employee_names = [name for (name,) in results]
    
    options = employee_names
    selected_option = request.form.get('option1')
    print(selected_option)
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return render_template('face_registration.html', options=options)

        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
       
                filename = secure_filename(file.filename)
                folder_path = UPLOAD_FOLDER + selected_option
                file_path = os.path.join(folder_path, filename)
           
                # Replace backslashes with forward slashes
                path_with_forward_slashes = file_path.replace('\\', '/')

                # Add 'C:' drive prefix
                final_path = 'C:' + path_with_forward_slashes

                
                # Create the folder if it doesn't exist
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Save the uploaded file

                # Resize the image to 120x120 pixels before saving

                img = Image.open(file)
                img.save(file_path)
                img2 = cv2.imread(final_path)

                random_filename = generate_random_filename()

                file_path = os.path.join(folder_path, random_filename+".jpg")

                results = model(img2)[0]

                H, W, _ = img2.shape
                
                
                for result in results.boxes.data.tolist():
                    
                    x1, y1, x2, y2, score, class_id = result
                    
                    print(score)
                    if score > threshold:
                        x1_cropped = int(max(0, x1 + margin))
                        y1_cropped = int(max(0, y1 + margin))
                        x2_cropped = int(min(W, x2 - margin))
                        y2_cropped = int(min(H, y2 - margin))

                        print(y2_cropped)
                        face_image = img2[y1_cropped:y2_cropped, x1_cropped:x2_cropped]
                        face_image_resized = cv2.resize(face_image, (120, 120))
                        #face_image_resized.save(file_path)

                        cv2.imwrite(file_path, face_image_resized)
                        print(file_path)
                        if os.path.exists(final_path):
                            os.remove(final_path)

                        print("Face cropped, resized, and saved")               

        flash('File(s) successfully uploaded', category='success')
        return render_template('face_registration.html', options=options)

    return render_template('face_registration.html', options=options)



@views.route('/run_python')
def run_python():
    
    # Execute the Python file
    subprocess.run(['python', '/Users/yunka/Desktop/New folder (5)/train-yolov8-custom-dataset-step-by-step-guide-master/local_env/train_model.py'])

    return 'Python file executed'

