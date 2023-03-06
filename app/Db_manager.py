from github import Github, Repository, GithubException
import uuid
import pprint
import datetime
# LINK= "moevm/mse_automatic_export_of_schedules_and_statistics"
LINK= "moevm/mse_automatic_export_of_schedules_and_statistics"
g = Github("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")
def NewUser(data):
    NUser={}
    NUser['UserName']=data['UserName']
    NUser['Password']=data['Password']
    NUser['Token']=data['Token']
    list=[]
    user = g.get_user(data['UserName'])
    for repo in user.get_repos():
        list.append(repo.name)

    NUser['Repos']=list
    #db_collection.insert_one(NUser)
    print(NUser)
    
def getComms(repo):
    #repo = g.get_repo(LINK)
    comms=[]
    commits=repo.get_commits()
    for commit in commits:
        com={'Id':"",'Author_Name':"",'Author_login':"",'Author_email':"",'Data_and_time':"",'Data_and_time':"",}
        com['Id']=commit.sha
        com['Author_Name']=commit.author.name if commit.author else ""
        com['Author_login']=commit.author.login if commit.author else ""
        com['Author_email']=commit.commit.author.email
        com['Data_and_time']=commit.commit.author.date.isoformat()
        com['Data_and_time']=commit.files
        comms.append(com)
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
        #pr['Id']=pull.id
        #pr['Title']=pull.title
        #pr['State']=pull.state
        pr['Commit_info']=comms
        pr['Creator_name']=pull.user.name
        pr['Creation_date']=pull.created_at.isoformat()
        pr['Creator_login']=pull.user.login
        pr['Creator_email']=pull.user.email
        pr['Changed_files']=pull.changed_files
        pr['Comments']=comments
        pr['Merger_login']=pull.merged_by.login
        pr['Merger_email']=pull.merged_by.email
        PRs.append(pr)
    return PRs
def NewRepoByURL():
    repo = g.get_repo(LINK)
    rt={}
    rt['Id']=uuid.uuid1()
    rt['Name']=repo.name
    rt['Issues']=getIssues(repo)
    rt['Commits']=getComms(repo)
    rt['Pull_Requests']=getPR(repo)
    pprint.pprint(rt)
    return
def NewRepo(data):
    repo={}
    repo['Id']=data['Id']
    repo['Name']=data['Name']
    repo['Issues']=data['Issues']
    repo['Commits']=data['Commits']
    repo['Pull_Requests']=data['Pull_Requests']
    #db_collection.insert_one(repo)
    return
dat={'UserName':"PsyholiricPavel",
     'Password':"123",
     'Token':"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",
     }
NewUser(dat)
NewRepoByURL()
#pprint.pprint(getIssues())
#pprint.pprint(getComms())
#pprint.pprint(getPR(LINK))

