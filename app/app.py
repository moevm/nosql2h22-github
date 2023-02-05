from flask import Flask, render_template, url_for, request
import pymongo
import random
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    #a = request.form['name']
    return render_template('main.html', value=random.random())

@app.route('/authorization', methods=['POST', 'GET'])
def name_sumbit():

    return render_template('authorization.html')

if __name__ == "__main__":
    app.run(debug=True)