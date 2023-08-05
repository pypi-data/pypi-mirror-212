from github import Github, InputGitTreeElement, Installation
import os
from dotenv import load_dotenv
from os.path import join, dirname
import webbrowser
import requests

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get("MANGO_TOKEN")
SECRET = os.environ.get("SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")

def get_token(text):
    # print(text)
    arr = text.split('&')
    tokens = {}
    for a in arr:
        t = a.split('=')
        tokens[t[0]] = t[1]
    return tokens


def get_user():
    g = Github(TOKEN)
    user = g.get_user()
    return user.login


def create_repo():
    g = Github(TOKEN)
    user = g.get_user()
    for repo in user.get_repos():
        if repo.name == 'portfolio':
            return

    user.create_repo(f"portfolio")
    os.system(f"dotenv set REPO {user.login}/portfolio")
    repo = g.get_repo(f"{user.login}/portfolio")
    repo.create_file("readme.md", "Add readme", "Hello!")


def auth():
    '''Authenticates the user if not already authenticated (token not found)'''
    token = TOKEN
    if not token:
        print("Creating token")
        r = requests.post(f'https://github.com/login/device/code?client_id={CLIENT_ID}')
        webbrowser.open('https://github.com/login/device')
        code = get_token(r.text)['device_code']
        print('Enter the user code below: ')
        print(get_token(r.text)['user_code'])
        ready = input('Press enter after entering code at GitHub')
        r = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={CLIENT_ID}&device_code={code}&grant_type=urn:ietf:params:oauth:grant-type:device_code")
        os.system(f"dotenv set MANGO_TOKEN {get_token(r.text)['access_token']}")

    print('Give access to bot')
    webbrowser.open('https://github.com/apps/mangowg-bot')
    print("Ready to use!")


def create_blobs(files, repo):
    '''Creates blobs for the files'''
    output = {}
    for file in files:
        f = open(file, 'r')
        output[file] = repo.create_git_blob(
            content=f.read(),
            encoding='utf-8',
        )
    return output


def create_tree(blobs, repo, master_sha):
    '''Creates a tree for the files'''
    tree = []
    for blob in blobs:
        tree.append(InputGitTreeElement(
            path=blob,
            mode="100644",
            type="blob",
            sha=blobs[blob].sha,
        ))
    return repo.create_git_tree(
        tree=tree,
        base_tree=repo.get_git_tree(master_sha)
    )


def update(files, repo_name=os.environ.get("REPO")):
    '''Updates the repo with the files'''
    g = Github(TOKEN)
    repo = g.get_repo(repo_name)
    blobs = create_blobs(files, repo)

    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha

    new_tree = create_tree(blobs, repo, master_sha)

    commit = repo.create_git_commit(
        message="Update portfolio",
        tree=repo.get_git_tree(sha=new_tree.sha),
        parents=[repo.get_git_commit(master_sha)],
    )

    master_ref.edit(sha=commit.sha)

def getGithubInfo():
    '''Returns the username of the authenticated user'''
    g = Github(TOKEN)

    userInfo = {
        "username": g.get_user().login,
        "profilePic": g.get_user().avatar_url,
        "bio": g.get_user().bio,
        "url": g.get_user().html_url,
    }

    return userInfo

def getRepoInfo():
    '''Returns the repo names of the authenticated user'''
    g = Github(TOKEN)

    repos = []

    for repo in g.get_user().get_repos():
        # get the repo name, about, and url
        repoInfo = {
            "name": repo.name,
            "about": repo.description,
            "url": repo.html_url,

            "display": False,
        }

        repos.append(repoInfo)

    return repos
