from github import Github, Repository, GithubException
import pprint
import datetime
import json
from pymongo import MongoClient

LINK= "PsyholiricPavel/MathPackages"
#LINK= "moevm/mse_automatic_export_of_schedules_and_statistics"
TOKEN="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"

client = MongoClient('localhost', 27017)

db = client["Data"] 
dbUsers = db["Users"]
dbRepos = db["Repos"]
#print("Available databases:", client.list_database_names())
#g = Github(TOKEN)
#repo = g.get_repo(LINK)
def isRegistredAlready(userN):
    return GetUser(userN)
def NewUser(data):
    NUser={}
    NUser['UserName']=data['UserName']
    NUser['Password']=data['Password']
    NUser['Token']=data['Token']
    list=[]
    #g = Github(NUser['Token'])
    #user = g.get_user(data['UserName'])
    #for repo in user.get_repos():
        #list.append(repo.name)
    NUser['Repos']=[]
    #NUser = json.dumps(NUser)
    a=dbUsers.insert_one(NUser)
    NUser['_id']=a.inserted_id
    return NUser   
def getComms(repo):
    #repo = g.get_repo(LINK)
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
        #dbCommits.insert_one(com)
    return comms
def getIssues(repo):
    #repo = g.get_repo(LINK)
    Iss=[]
    issues = repo.get_issues(state='all')
    
    for issue in issues:
        comments=[]
        for comment in issue.get_comments():
            comment_i={}
            #print(comment.body)
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
        #dbIssues.insert_one(el)
    return Iss
def getPR(repo):
    #repo = g.get_repo(LINK)
    PRs=[]
    pulls=repo.get_pulls(state='all')
    
    #print()
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
    if len(list(dbRepos.find({'Name':repo.name})))!=0:
        dbUsers.update_one({"_id":user["_id"]},{'$addToSet':{'Repos':rt['Name']}})
    rt={}
    rt['Name']=repo.name
    rt['Issues']=getIssues(repo)
    rt['Commits']=getComms(repo)
    rt['Pull_Requests']=getPR(repo)
    #pprint.pprint(rt)
    #rt = json.dumps(rt)
    dbRepos.insert_one(rt)
    user['Repos'].append(repo.name)
    dbUsers.update_one({"UserName":user["UserName"]},{'$addToSet':{'Repos':rt['Name']}}) # $addToSet
    #pprint.pprint(user)
    return
def NewRepo(data):
    repo={}
    repo['Id']=data['Id']
    repo['Name']=data['Name']
    repo['Issues']=data['Issues']
    repo['Commits']=data['Commits']
    repo['Pull_Requests']=data['Pull_Requests']
    #dbRepos.insert_one(repo)
    return
def DeleteRepo(name,user):
     dbUsers.update_one({'Repos':name, 'UserName':user['UserName']},{'$pull':{'Repos':name}})
     if len(list(dbUsers.find({'Repos':name})))==0:
         dbRepos.delete_one({'Name':name})
     return   
def GetReposOfUser(userN):
    cursor =dbUsers.find_one({'UserName': userN})
    print(cursor['Repos'])
    repos=[]
    for repo in cursor['Repos']:
        repos.append(dbRepos.find_one({'Name':repo}))
    return repos
def GetUser(userN):
    cursor =dbUsers.find_one({'UserName': userN})
    return cursor
def LogUser(data):
    cursor =dbUsers.find_one({'UserName': data['login']})
    if "Password" not in data or not data['Password']:
        return "No Password"
    if cursor['Password']!= data['Password']:
        return "Wrong Password"
    else:
        return "OK"
dat={
    'UserName':"zmm",
     'Password':"123",
     'Token':TOKEN,
     }
dat2={
    'login':"PsyholiricPavel",
     'Password':"124",
     }
dat3={
    'login':"PsyholiricPavel",
     'Password':"123",
     }
dat4={
    'login':"PsyholiricPavel"
     }
#user=NewUser(dat)
#user=GetUser('PsyholiricPavel')
#NewRepoByURL("PsyholiricPavel/AiSD",user)
#NewRepoByURL("PsyholiricPavel/Ford_Uorshell",user)
#NewRepoByURL("PsyholiricPavel/MathPackages",user)
#NewRepoByURL("PsyholiricPavel/nosql2h22-github",user)
#NewRepoByURL("PsyholiricPavel/Practice-",user)
#print("==============================\n",GetUser('PsyholiricPavel'),"\n==============================\n")
#pprint.pprint(GetReposOfUser('PsyholiricPavel'))
#DeleteRepo('MathPackages',user)
print('aaaa')
