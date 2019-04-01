from flask import Flask,render_template,request
import pymysql as dbc
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import time
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/', methods=['POST'])
def get_val():
    '''if request.form['ShowReviews'] == 'ShowReviews':
        return render_template('retrieve.html')
    else:
    name = request.form['name']
    name = str(name)'''
    mail = request.form['email']
    mail = str(mail)
    file = open(r'C:\Users\npt19\PycharmProjects\DataAnalytics and ML\Login\authentication.txt','r')
    name = file.readline()
    name = str(name)
    #mail = 'npt1998@gmail.com'
    manufacturer = request.form['Manufacturer']
    manufacturer = str(manufacturer)
    product = request.form['Product']
    product = str(product)
    EnginePerformance = request.form['message1']
    EnginePerformance = str(EnginePerformance)
    Dynamics = request.form['message2']
    Dynamics = str(Dynamics)
    Handling = request.form['message3']
    Handling = str(Handling)
    analysis = SentimentIntensityAnalyzer()
    EngineScore = analysis.polarity_scores(EnginePerformance)
    DynamicScore = analysis.polarity_scores(Dynamics)
    HandlingScore = analysis.polarity_scores(Handling)
    EnglineScoreList,DynamicScoreList,HandlingScoreList = list(EngineScore.values()),list(DynamicScore.values()),list(HandlingScore.values())
    EngineScoreFinal,DynamicScoreFinal,HandlingScoreFinal = float(EnglineScoreList[3]),float(DynamicScoreList[3]),float(HandlingScoreList[3])
    OverAllScore = EngineScoreFinal + DynamicScoreFinal + HandlingScoreFinal
    OverAllScore = OverAllScore / 3
    OverAllScore = float(OverAllScore)
    conn = dbc.connect(host='localhost', user='root', passwd='', db='sentiment')
    Mycursor = conn.cursor()
    param = [name,mail,manufacturer,product,EnginePerformance,Dynamics,Handling,EngineScoreFinal,DynamicScoreFinal,HandlingScoreFinal,OverAllScore]
    paramfinal = []
    for i in param:
        i = str(i)
        paramfinal.append(i)
    querry = "INSERT INTO " + name + "(Username,EmailID,Manufacturer,Product,EnginePerformance,Dynamics,Handling,EngineScore,DynamicsScore,HandlingScore,OverAllPerformance) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    Mycursor.execute(querry,tuple(paramfinal))
    ret = 'Database successful'
    conn.commit()
    Mycursor.execute("SELECT * FROM "+name)
    records = Mycursor.fetchall()
    conn.close()
    Username,EmailID,Manufacturer,Product,EnginePerformance,Dynamics,Handling,EngineScore,DynamicsScore,HandlingScore,OverAllPerformance = [],[],[],[],[],[],[],[],[],[],[]
    for row in records:
        Username.append(row[0])
        EmailID.append(row[1])
        Manufacturer.append(row[2])
        Product.append(row[3])
        EnginePerformance.append(row[4])
        Dynamics.append(row[5])
        Handling.append(row[6])
        EngineScore.append(row[7])
        DynamicsScore.append(row[8])
        HandlingScore.append(row[9])
        OverAllPerformance.append(row[10])
    dict1 = {'Username':Username,'EmailID':EmailID,'Manufacturer':Manufacturer,'Product':Product,'EnginePerformance':EnginePerformance,'Dynamics':Dynamics,'Handling':Handling,'EngineScore':EngineScore,'DynamicsScore':DynamicsScore,'HandlingScore':HandlingScore,'OverAllPerformance':OverAllPerformance}
    #dict1 = {'Manufacturer':Manufacturer,'Product':Product,'EnginePerformance':EnginePerformance,'Dynamics':Dynamics,'Handling':Handling,'EngineScore':EngineScore,'DynamicsScore':DynamicsScore,'HandlingScore':HandlingScore,'OverAllPerformance':OverAllPerformance}
    df = pd.DataFrame(dict1)
    df.to_html(r'C:\Users\npt19\PycharmProjects\DataAnalytics and ML\templates\retrieve.html')
    time.sleep(1)
    return render_template('retrieve.html')
if __name__ == '__main__':
   app.run(debug = True)
