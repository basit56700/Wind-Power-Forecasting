from flask import Flask, request, jsonify, render_template
import requests
import json
import pandas as pd
from sklearn.linear_model import LinearRegression

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "8r_73r_kobxkRh4xVZMTU29nikPAwCq3_2et93LJDKCj"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)
#model = joblib.load('power_prediction.sav')

newtime = []
values2 = []
labels = []
values1 = []
theo = []
predict = []
speeds=[]
labels1=[]

@app.route('/')
def home():
    return render_template('intro.html')


@app.route('/predict')
def predict():
    values=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
    labels=['01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '23:00', '24:00']
    return render_template('predict.html', values1 = values,labels=labels,values2=values)

@app.route('/windapi',methods=['POST'])
def windapi():
    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    city= request.form['city']
    theo= request.form['theo']
    querystring = {"q":city+",pk"}


    headers = {
   	"X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
   	"X-RapidAPI-Key": "192c168bfamsh95b0276211bb318p1eb036jsn7458df0ef51f"
       }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_response = json.loads(response.text)
    #print(json_response)
  
    pre=[]
    for weather in json_response['list']:
        speed = float((weather["wind"]["speed"])*3.6)
        pred = ([(float((weather["wind"]["speed"]))),(theo)])
        dt_txt = str(weather["dt_txt"])
        dt_txt = dt_txt.split()
        time = [dt_txt[1]]
        newtime.append(time)
        pre.append(pred)
        speeds.append(speed)
    labels = newtime
    values = speeds
    predict= pre
    
    predict=predict[:20]
    values1=values[:20]
    labels1=labels[:20]
    values2=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
    df = pd.read_csv("T1.csv")
    df = df.round(decimals = 6)
    x= df.drop(["LV ActivePower (kW)","Date/Time","Wind Direction (°)"], axis =1)
    y= df.drop(["Theoretical_Power_Curve (KWh)","Wind Speed (m/s)","Date/Time","Wind Direction (°)"], axis =1)
    clf = LinearRegression().fit(x, y)
    values2 = clf.predict(predict)
    values2 = values2.tolist()
    val=[]
    for xs in values2:
        for x in xs:
            val.append(x)
        
        values2 = val
        
    Sum = int(sum(values2))
    print(Sum)
    
    
    
    return render_template('predict.html', values1=values1,labels=labels1,values2=values2,Sum=Sum)  
  
   

if __name__ == "__main__":
    app.run(debug=False)
