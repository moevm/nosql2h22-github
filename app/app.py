<<<<<<< HEAD
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
=======
from flask import Flask, render_template, url_for
import pymongo
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('main.html', value=12)


if __name__ == "__main__":
>>>>>>> 465d9a129140fe0110168e4abae78fb3a3d433c0
    app.run(debug=True)