from flask import Flask, render_template,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/',methods = ['GET'])
def home():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
	return(jsonify(200))

@app.route('/check/', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        url = request.form['url']
        print(url)
        return render_template('index.html')
    else:
        return render_template('index.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, threaded=True)