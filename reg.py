from flask import Flask,render_template,request,redirect
import pymysql as dbc
import time
import pandas as pd
conn = dbc.connect(host='localhost', user='root', passwd='', db='sentiment')
#conn2 = dbc.connect(host='localhost',user='root',passwd = '',db = 'login_signup')
Mycursor = conn.cursor()
#Mycursor2 = conn2.connect()
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/', methods=['POST'])
def get_details():
    first_name = request.form['first_name']
    first_name = str(first_name)
    last_name = request.form['last_name']
    last_name = str(last_name)
    name = first_name + last_name
    Email = request.form['email']
    Email = str(Email)
    password = request.form['password']
    password = str(password)
    ph_number = request.form['phone']
    ph_number = int(ph_number)
    Mycursor.execute('SHOW TABLES')
    table = Mycursor.fetchall()
    table_names = []
    for i in table:
        i = str(i)
        table_names.append(i)
    table_names = [i[2:-3] for i in table_names]
    if name in table_names:
        return 'Existing account'
    else:
        df = pd.read_csv('login_signup.csv')
        df = pd.DataFrame(df)
        username = list(df['Username'])
        Pass = list(df['Password'])
        email = list(df['Email'])
        Phone = list(df['PhoneNumber'])
        username.append(name)
        Pass.append(password)
        email.append(Email)
        Phone.append(ph_number)
        df_final = {'Username':username,'Email':email,'Password':Pass,'PhoneNumber':Phone}
        df_final = pd.DataFrame(df_final)
        df_final.to_csv('login_signup.csv')
        time.sleep(1)
        querry = "CREATE TABLE " + name + " (Username TEXT(100),EmailID TEXT(100),Manufacturer TEXT(500),Product TEXT(500),EnginePerformance TEXT(500),Dynamics TEXT(500),Handling TEXT(500),EngineScore float(5),DynamicsScore float(5),HandlingScore float(5),OverAllPerformance float(5));"
        Mycursor.execute(querry)
        conn.commit()
        return redirect('http://127.0.0.1:4010/')
if __name__ == '__main__':
   app.run(debug = True,port=4020)
