from flask import Flask, render_template, url_for, request, redirect
from Db_manager import *
import pprint
links = [{'name': 'link_1'},
             {'name': 'link_2'}]

user = {}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in 'json'

@app.route('/', methods=['GET'])
def home():
    return redirect('authorization')

@app.route('/authorization', methods=['POST', 'GET'])
def authorization():
    global user
    if(user == {}):
        valid_reg= True
        valid_login = True
        ImportFromJSON("no", 'u')
        ImportFromJSON("no1", 'r')
        if request.method == "POST":
            f_users = {}
            f_repos = {}
            if (request.form.get('users-alert')== 'True'):
                f_users = request.files['upload-user']
                if allowed_file(f_users.filename):
                    ImportFromJSON("no", 'u')
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
            RegUser = {'UserName': RegUsername,
                        'Password': RegPassword,
                        'Token': RegToken}
            if((RegUsername == '') or
                (RegPassword == '') or
                (RegToken == '')):
                valid_reg = False
                print('3')
            else:
                if ((RegUsername != None) or
                    (RegPassword != None) or
                    (RegToken != None)):
                    if (isRegistredAlready(RegUser['UserName'])):
                        valid_reg = False
                        print('2')
                    elif (TokenValidator(RegUser) == [False,"Not your token"]):
                        valid_reg = False
                        print('1')
                    else:
                        NewUser(RegUser)
            LoginUsername = request.form.get('LoginUsername')
            LoginPassword = request.form.get('LoginPassword')
            LoginUser = {'login': LoginUsername,
                            'Password': LoginPassword}
            if ((LoginUsername == '') or (LoginPassword == '')):
                valid_login = False
            else:
                if ((LoginUsername != None) or (LoginPassword != None)):
                    tmp_user, message = Authorization(LoginUser)
                    if (message != "OK"):
                        valid_login = False
                    else:
                        user = tmp_user
                        print(user)   
                        return redirect('menu')

        return render_template('authorization.html', valid_reg=valid_reg, valid_login=valid_login)
    else:
        return redirect('menu')

@app.route('/menu', methods=['POST', 'GET'])
def menu():
    global user
    if user == {}:
        return redirect('authorization')
    else:
        if request.method == "POST":
            LogOut = request.form.get('LogOut')
            if LogOut != None:
                if LogOut == "1":
                    user = {}
                    return redirect('authorization')
            AddRepoName = request.form.get('RepoName')
            if AddRepoName != None:
            #проверка на валидность
                NewRepoByURL(AddRepoName,user)
                print(AddRepoName)
                links.append({'name': AddRepoName})
            DelRepo = request.form.get('del-this-repo')
            if DelRepo != None:
                DeleteRepo(DelRepo,user)
                print(DelRepo)
   
        repos = GetReposOfUserDB(user['UserName'])
        name = user['UserName']
        issues = {}
        pr = {}
        commits = {}
        for i in repos:
            issues[i] = OutTable(i,"Issues")
            pr[i] = OutTable(i,"Pull_Requests")
            commits[i] = OutTable(i,"Commits")
        pprint.pprint(issues)
        return render_template('menu.html',repos=repos, name=name, issues=issues, prs=pr, commits=commits)

if __name__ == "__main__":
    app.run(debug=True)


    # Таблицы
    # Скачивание
    # Досвязать регу
    #