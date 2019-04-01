from flask import Flask,render_template,request,redirect
import pymysql as dbc
import pandas as pd
conn = dbc.connect(host='localhost', user='root', passwd='', db='sentiment')
conn2 = dbc.connect(host='localhost',user='root',passwd = '',db = 'login_signup')
Mycursor = conn.cursor()
Mycursor2 = conn2.connect()
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/', methods=['POST'])
def get_val():
    name = request.form['email']
    name = str(name).lower()
    password = request.form['pass']
    password = str(password)
    Mycursor.execute('SHOW TABLES')
    table = Mycursor.fetchall()
    table_names = []
    for i in table:
        i = str(i)
        table_names.append(i)
    table_names = [i[2:-3] for i in table_names]
    if name in table_names:
        df = pd.read_csv(r'C:\Users\npt19\PycharmProjects\DataAnalytics and ML\Signup\login_signup.csv')
        df = pd.DataFrame(df)
        for x in df['Username'].tolist():
            if x == name:
                break
        pass_check = df.loc[df['Username'] == name, 'Password'].iloc[0]
        if str(pass_check) == password:
            file1 = open('authentication.txt','w')
            file1.write(name)
            return redirect('http://127.0.0.1:5000/')
        else:
            return 'Incorrect username'
if __name__ == '__main__':
   app.run(debug = True,port=4010)
