from flask import Flask, render_template, url_for, request, redirect
#from Db_manager import *
LINKS = [
    {'name': 'github', 'url': 'https://github.com/'}
]
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return redirect('authorization')

@app.route('/authorization', methods=['POST', 'GET'])
def authorization():
    valid_reg= True
    valid_login = True
    if request.method == "POST":
        RegUsername = request.form.get('RegUsername')
        RegPassword = request.form.get('RegPassword')
        RegToken = request.form.get('Token')
        RegUser = [{'UserName': RegUsername},
                   {'Password': RegPassword},
                   {'Token': RegToken}]
        if((RegUsername == '') or
            (RegPassword == '') or
            (RegToken == '')):
            valid_reg = False
        else:
            if ((RegUsername != None) or
            (RegPassword != None) or
            (RegToken != None)):
                print("Reg")
        LoginUsername = request.form.get('LoginUsername')
        LoginPassword = request.form.get('LoginPassword')
        LoginUser = [{'UserName': LoginUsername},
                     {'Password': LoginPassword}]
        if ((LoginUsername == '') or (LoginPassword == '')):
            valid_login = False
        else:
            if ((LoginUsername != None) or (LoginPassword != None)):
                print("Logined")

    return render_template('authorization.html', valid_reg=valid_reg, valid_login=valid_login)

@app.route('/menu', methods=['POST', 'GET'])
def menu():
    links = [{'name': 'link_1'},
             {'name': 'link_2'}, ]
    if request.method == "POST":
        AddRepoName = request.form.get('RepoName')
        print(AddRepoName)
        

    stat = {'links': links,
            'user_name': 'Username'}
    
    return render_template('menu.html',
                           stats=stat)

if __name__ == "__main__":
    app.run(debug=True)