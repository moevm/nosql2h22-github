from flask import Flask, render_template, url_for, request, redirect
#from Db_manager import *
links = [{'name': 'link_1'},
             {'name': 'link_2'}]
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in 'json'

@app.route('/', methods=['GET'])
def home():
    return redirect('authorization')

@app.route('/authorization', methods=['POST', 'GET'])
def authorization():
    valid_reg= True
    valid_login = True
    if request.method == "POST":
        f_users = {}
        f_repos = {}
        if (request.form.get('users-alert')== 'True'):
            f_users = request.files['upload-user']
            if f_users != '':
                if allowed_file(f_users.filename):
                    print("json!")
        if (request.form.get('repo-alert')== 'True'):
            f_repos = request.files['upload-repos']
            if allowed_file(f_repos.filename):
                print("json!")
        Download = request.form.get('download')
        if Download == 'True':
            #скачать
            print('download')    

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
                # Пользователь ввел какие-то данные для рега
                print("Reg")
        LoginUsername = request.form.get('LoginUsername')
        LoginPassword = request.form.get('LoginPassword')
        LoginUser = [{'UserName': LoginUsername},
                     {'Password': LoginPassword}]
        if ((LoginUsername == '') or (LoginPassword == '')):
            valid_login = False
        else:
            if ((LoginUsername != None) or (LoginPassword != None)):
                # Пользователь идет на проверку логина и парола
                print("Logined")
                return redirect('menu')

    return render_template('authorization.html', valid_reg=valid_reg, valid_login=valid_login)

@app.route('/menu', methods=['POST', 'GET'])
def menu():
    if request.method == "POST":
        LogOut = request.form.get('LogOut')
        if LogOut != None:
            if LogOut == "1":
                # обнулнение User 
                print("a")
                return redirect('authorization')
        AddRepoName = request.form.get('RepoName')
        if AddRepoName != None:
            #добавление репо
            print(AddRepoName)
            links.append({'name': AddRepoName})
        DelRepo = request.form.get('del-this-repo')
        if DelRepo != None:
            #удаление репо
            print(DelRepo)
    stat = {'links': links,
            'user_name': 'Username'}
    
    return render_template('menu.html',
                           stats=stat)

if __name__ == "__main__":
    app.run(debug=True)