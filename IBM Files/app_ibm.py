
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "fW2yZPgle7_vDz4rsBmBJsiyyEOC7vNHmxCeCio6rm01"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[int(x) for x in request.form.values()]]
    print(x_test)
    
    # payload_scoring = {"input_data": [{"fields": [["year", "month", "day"]], "values": [[2005,7,23]]}]}
    payload_scoring = {"input_data": [{"fields": [["year", "month", "day"]], "values": x_test}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b2bbff7f-2a48-4e56-b29b-9116ea5e7f24/predictions?version=2022-03-06', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred= response_scoring.json()
    print(pred)
    
    output = pred['predictions'][0]['values'][0][0]
    print(output)
  
    return render_template('index.html', prediction_text='Gas Price is {} Dollars'.format(output))

if __name__ == "__main__":
    app.run(port="8000",debug=False)
