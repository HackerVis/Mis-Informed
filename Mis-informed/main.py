from flask import Flask, render_template,request,jsonify # Importing the Flask module
from flask_cors import CORS # Importing the CORS module
from Mis_informed import * # Importing the Mis_informed.py file

app = Flask(__name__) # Creating a Flask object
CORS(app) # Enabling CORS


@app.route('/',methods = ['GET']) # The route for the home page
def home():
    return render_template('index.html') # The home page

@app.route('/status', methods=['GET']) # The route for the status page
def status():
	return(jsonify(200))

@app.route('/check/', methods=['GET', 'POST']) # The route for the check page
def check(): 
    if request.method == 'POST': 
        url = request.form['url']
        site = url
        informative_percent, safetyResult, domain_name = getMisinformation(site)
        return render_template('result.html', site = domain_name, informative_percent = informative_percent, safetyResult = safetyResult) # The check page
    else:
        return render_template('index.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, threaded=True)