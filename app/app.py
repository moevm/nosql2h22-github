from flask import Flask, render_template, url_for, request
import pymongo
import random
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('main.html', value=random.random())

@app.route('/name_sumbit', methods=['POST', 'GET'])
def name_sumbit():
    a = request.form['name']
    return render_template('name_sumbit.html', name=a)


if __name__ == "__main__":
    app.run(debug=True)