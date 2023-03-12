from flask import Flask, render_template, url_for, request, redirect
import pymongo
import random
LINKS = [
    {'name': 'github', 'url': 'https://github.com/'}
]
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():

    return redirect('authorization')

@app.route('/authorization', methods=['POST', 'GET'])
def authorization():

    return render_template('authorization.html')

@app.route('/menu', methods=['POST', 'GET'])
def statistic():
    links = [{'name': 'link_1'},
             {'name': 'link_2'}, ]
    stat = {'links': links,
            'user_name': 'Username'}
    
    return render_template('menu.html',
                           stats=stat)

if __name__ == "__main__":
    app.run(debug=True)