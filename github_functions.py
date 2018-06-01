import requests
from flask import request, json
from request_urls import add_label_url, send_team_invite, assign_issue_url, check_assignee_url
from auth_credentials import USERNAME,PASSWORD, newcomers_team_id

#request headers
headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/x-www-form-urlencoded'}

#labels newly opened issues with "Not Approved" tag
def label_opened_issue(data):
    session = requests.Session()
    #create a authenticated session
    session.auth = (USERNAME, PASSWORD)
    #extract issue and repo data from webhook's response
    issue_number = data.get('issue',{}).get('number',-1)
    repo_name = data.get('repository',{}).get('name','')
    repo_owner = data.get('repository',{}).get('owner',{}).get('login',"")
    #raw body( string ) with list of tags
    label = '["Not Approved"]'
    #construct the request url
    request_url = add_label_url % (repo_owner, repo_name,issue_number)
    if issue_number !=-1 and repo_name !="" and repo_owner!="":
        #send request
        r = session.post(request_url, data=label, headers=headers)
        #check response
        if r.status_code == 201:
            print('Success')
            return {'message':'Success', 'status':r.status_code}
        else:
            print(r.content)
            return {'message':'Error', 'status':r.status_code}
    return {'message':'Format of data provided is wrong or misformed', 'status': 400}


def send_github_invite(github_id):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    #Header as required by Github API
    headers = {'Accept': 'application/vnd.github.hellcat-preview+json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    request_url =  send_team_invite %(newcomers_team_id, github_id)
    r = session.put(request_url, data=json.dumps({'role': 'member'}), headers=headers)
    if r.status_code == 200:
        return {'message':'Success', 'status':r.status_code}
    else:
        return {'message':'Error', 'status':r.status_code}
    return {'message':'Data provided is wrong', 'status': 400}


def issue_comment_approve_github(issue_number, repo_name, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    #Name of label to be removed
    remove_label_name = '/Not%20Approved'
    #Label to be added
    label = '["issue-approved"]'
    request_url = add_label_url % (repo_owner, repo_name, issue_number)
    #Delete the not approved label first
    response = session.delete(request_url+remove_label_name, headers=headers)
    if response.status_code == 200 or response.status_code == 404:
        #Add the new label
        response = session.post(request_url, data=label, headers=headers)
        if response.status_code == 200:
            return {'message':'Success', 'status':response.status_code}
        else:
            return {'message':'Error', 'status':response.status_code}
    return {'message':'Data provided is wrong', 'status': 400}


def github_pull_request_label(pr_number, repo_name, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/x-www-form-urlencoded'}
    label = '["under review"]'
    #Add label of under review to new PRs
    request_url = add_label_url % (repo_owner, repo_name, pr_number)
    response = session.post(request_url, data=label, headers=headers)
    return response.status_code


def issue_assign(issue_number, repo_name, assignee, repo_owner):
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json', 'Content-Type': 'application/json'}
    label = '{"assignees": ["%s"]}' % assignee
    #Request to assign the issue
    request_url = assign_issue_url % (repo_owner, repo_name, issue_number)
    response = session.patch(request_url, data=label, headers=headers)
    return response.status_code

def check_assignee_validity(repo_name, assignee, repo_owner):
    request_url = check_assignee_url % (repo_owner, repo_name, assignee)
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    response = session.get(request_url)
    return response.status_code
