from github import Github, Repository, GithubException
import pprint
import datetime
import json
from pymongo import MongoClient, InsertOne
import bson.json_util as json_util

client = MongoClient('localhost', 27017)

db = client["Data"] 
dbUsers = db["Users"]
dbRepos = db["Repos"]
def TokenValidator(user):
    g = Github(user['Token'])
    try:
        u=g.get_user()
        u.id
    except GithubException:
        return [False,"BadToken"]
    else:
        if user['UserName']!=u.login:
            return [False,"Not your token"]
        else:
            return [True,"GoodToken"]
def isRegistredAlready(userN):
    return GetUser(userN)!=None
def Authorization(data):
    cursor =dbUsers.find_one({'UserName': data['login']})
    if not isRegistredAlready(data['login']):
        return [None,"Not registred"]
    if "Password" not in data or not data['Password']:
        return [None,"No Password"]
    if cursor['Password']== data['Password']:
        return [cursor,"OK"]
    else:
        return [None,"Wrong Password"]
def NewUser(data):
    NUser={}
    NUser['UserName']=data['UserName']
    NUser['Password']=data['Password']
    NUser['Token']=data['Token']
    list=[]
    NUser['Repos']=[]
    a=dbUsers.insert_one(NUser)
    NUser['_id']=a.inserted_id
    return NUser   
def getComms(repo):
    comms=[]
    commits=repo.get_commits()
    for commit in commits:
        files=[]
        com={'Id':"",'Author_Name':"",'Author_login':"",'Author_email':"",'Data_and_time':"",'Data_and_time':"",}
        com['Id']=commit.sha
        com['Author_Name']=commit.author.name if commit.author else ""
        com['Author_login']=commit.author.login if commit.author else ""
        com['Author_email']=commit.commit.author.email if commit.commit.author else ""
        com['Data_and_time']=commit.commit.author.date.isoformat() if commit.commit.author else ""
        for file in commit.files:
            files.append(file.filename)
        com['Changed files']=files
        comms.append(com)
    return comms
def getIssues(repo):
    Iss=[]
    issues = repo.get_issues(state='all')
    
    for issue in issues:
        comments=[]
        for comment in issue.get_comments():
            comment_i={}
            comment_i['Comment_date']=comment.created_at.isoformat() 
            comment_i['Comment_body']=comment.body
            comment_i['Comment_author_name']=comment.user.name 
            comment_i['Comment_author_login']=comment.user.login
            comment_i['Comment_author_email']=comment.user.email
            comments.append(comment_i)
        el={}
        el['Id']=issue.id
        el['Number']=issue.number
        el['Title']=issue.title
        el['State']=issue.state
        el['Task']=issue.body
        el['Creation_date']=issue.created_at.isoformat()
        el['Creator_name']=issue.user.name
        el['Creator_login']=issue.user.login
        el['Creator_email']=issue.user.email
        #el['Changed_files']=issue как в ишью могут меняться файлы???
        el['Comments']=comments
        Iss.append(el)
    return Iss
def getPR(repo):
    PRs=[]
    pulls=repo.get_pulls(state='all')
    for pull in pulls:
        comms=[]
        for comm in pull.get_commits():
            comms.append(comm.sha)
        comments=[]
        for comment in pull.get_comments():
            comment_i={}
            comment_i['Comment_body']=comment.body
            comment_i['Comment_created_date']=comment.created_at.isoformat()
            comment_i['Comment_author_name']=comment.user.name
            comment_i['Comment_author_login']=comment.user.login
            comment_i['Comment_author_email']=comment.user.email
            comments.append(comment_i)
        pr={}
        pr['Id']=pull.id
        pr['Title']=pull.title
        pr['State']=pull.state
        pr['Commit_info']=comms
        pr['Creator_name']=pull.user.name
        pr['Creation_date']=pull.created_at.isoformat()
        pr['Creator_login']=pull.user.login
        pr['Creator_email']=pull.user.email
        pr['Changed_files']=pull.changed_files
        pr['Comments']=comments
        pr['Merger_login']=pull.merged_by.login if pull.merged_by else ""
        pr['Merger_email']=pull.merged_by.email if pull.merged_by else ""
        PRs.append(pr)
    return PRs
def NewRepoByURL(rref,user):
    g = Github(user['Token'])
    repo = g.get_repo(rref)
    rt={}
    rt['Name']=repo.name
    if len(list(dbRepos.find({'Name':repo.name})))!=0:
        dbUsers.update_one({"_id":user["_id"]},{'$addToSet':{'Repos':rt['Name']}})
    rt['Issues']=getIssues(repo)
    rt['Commits']=getComms(repo)
    rt['Pull_Requests']=getPR(repo)
    dbRepos.insert_one(rt)
    user['Repos'].append(repo.name)
    dbUsers.update_one({"UserName":user["UserName"]},{'$addToSet':{'Repos':rt['Name']}}) # $addToSet
    return
def DeleteRepo(name,user):
     dbUsers.update_one({'Repos':name, 'UserName':user['UserName']},{'$pull':{'Repos':name}})
     if len(list(dbUsers.find({'Repos':name})))==0:
         dbRepos.delete_one({'Name':name})
     return   
def GetReposOfUserGH(userN):
    cursor =dbUsers.find_one({'UserName': userN})
    print(cursor['Repos'])
    repos=[]
    for repo in cursor['Repos']:
        repos.append(dbRepos.find_one({'Name':repo}))
    return repos
def GetReposOfUserDB(userN):
    cursor =dbUsers.find_one({'UserName': userN})
    return cursor['Repos']
def GetUser(userN):
    cursor =dbUsers.find_one({'UserName': userN})
    return cursor
def ExportToJSON(filename,whichBase='r'):
    base =dbUsers if whichBase=='u' else dbRepos
    cursor=base.find()
    with open('jsons/'+filename+'.json', 'w', encoding="utf-8") as f:
        f.write(json_util.dumps(cursor,indent=4))
    return
def ImportFromJSON(filename,whichBase='r'):
    base =dbUsers if whichBase=='u' else dbRepos
    requesting = []

    with open('jsons/'+filename+'.json',) as f:
        file_data = json.load(f)
    for dt in file_data:
        del dt['_id']
    if isinstance(file_data, list):
        base.insert_many(file_data) 
    else:
        base.insert_one(file_data)
    return
def OutTable(name,want):
    cursor =dbRepos.find_one({'Name': name})
    return cursor[want]

#валидацию Гита! импорт на файл !Экспорт файл