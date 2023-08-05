import json
import DataScraper
import TemplateGeneratorYattag

from pprint import pprint
import inquirer

import time
import typer
from rich.progress import track

app = typer.Typer()

userData = {}
reposData = []
githubUserData = {}

##### Github Setup #####
@app.command("start")
def start():
    """Starts the program"""
    print("Welcome!")
    print("Authenticating")
    DataScraper.auth()

@app.command("new")
def new():
    """Creates a new repo: Portfolio"""
    DataScraper.create_repo()

@app.command("push")
def push():
    """Pushes the files in the util folder to your GitHub repository"""
    files = ['index.html']
    DataScraper.update(files)
    print("Success!")

##### Data Selection #####

@app.command("getRepos")
def getRepos():
    '''Gets all the repositories in your Github account'''
    reposData = DataScraper.getRepoInfo()
    # print(reposData)

    # Save the data to a json file
    with open('reposData.json', 'w') as outfile:
        json.dump(reposData, outfile)

@app.command("getGithubInfo")
def getGithubInfo():
    '''Gets your Github account information'''
    githubUserData = DataScraper.getGithubInfo()
    # print(githubUserData)

    # Save the data to a json file
    with open('githubUserData.json', 'w') as outfile:
        json.dump(githubUserData, outfile)

@app.command("updateTemplate")
def updateTemplate():
    '''Updates the template with the data'''
    print("Loading data... ")

    for value in track(range(3), description="Processing..."):
        if value == 0:
            # Load the data from the json files
            with open('userData.json') as json_file:
                userData = json.load(json_file)

        if value == 1:
            with open('reposData.json') as json_file:
                reposData = json.load(json_file)

        if value == 2:
            with open('githubUserData.json') as json_file:
                githubUserData = json.load(json_file)

    print("Updating template... ")

    TemplateGeneratorYattag.generateNewHTML(userData, reposData, githubUserData)

    print("Template Updated!")


@app.command("selectRepos")
def selectRepos():
    '''Selects the repositories to be displayed in your portfolio'''
    print("Selecting repos... ")

    with open('reposData.json') as json_file:
        reposData = json.load(json_file)

    if len(reposData) == 0:
        print("You have no repos!")
        return
    
    repoNames = []
    for repo in reposData:
        repoNames.append(repo['name'])

    # Use Inquirer to ask the user if they want to include the repo in their portfolio
    questions = [
        inquirer.Checkbox('repos',
                            message="Select the repos you want to include in your portfolio",
                            choices=repoNames,
                        ),
    ]

    answers = inquirer.prompt(questions)
    # print(answers["repos"])

    for repo in reposData:
        if repo['name'] in answers["repos"]:
            repo['display'] = True
        else:
            repo['display'] = False

    # Save the data to a json file
    with open('reposData.json', 'w') as outfile:
        json.dump(reposData, outfile)

    print("Selection Updated!")


@app.command("updateWholeProfile")
def updateUserData():
    '''Updates all the user data at once'''
    print("Updating profile... ")

    userData = {
        "socialMedia": {}
    }

    print("Enter your name: ")
    userData['name'] = input()
    print("Enter your email: ")
    userData['email'] = input()
    print("Enter your phone number: ")
    userData['phone'] = input()
    print("Enter your about: ")
    userData['about'] = input()
    print("Enter your twitter handle [optional]: ")
    userData['socialMedia']['twitter'] = input()
    print("Enter your facebook handle [optional]: ")
    userData['socialMedia']['facebook'] = input()
    print("Enter your instagram handle [optional]: ")
    userData['socialMedia']['instagram'] = input()

    # Save the data to a json file
    with open('userData.json', 'w') as outfile:
        json.dump(userData, outfile)

    print("Profile Updated!")


@app.command("updateProfileDetails")
def updateUserDataIndividually():
    '''Lets the user select which data to update'''

    # Load the data from the json files
    with open('userData.json') as json_file:
        userData = json.load(json_file)

    questions = [
        inquirer.List(
            "value",
            message="Select which data field to update",
            choices=["name", "email", "phone", "bio", "about", "twitter", "facebook", "instagram"],
        ),
    ]

    answers = inquirer.prompt(questions)

    print("Enter the new " + answers["value"] + ": ")
    userData[answers["value"]] = input()

    # Save the data to a json file
    with open('userData.json', 'w') as outfile:
        json.dump(userData, outfile)

@app.command("cut")
def selectComamand():
    '''Shortcut to select the command to be executed instead of typing it'''
    commandNames = []
    for command in app.registered_commands:
        commandNames.append(command.name)

    questions = [
        inquirer.List(
            "value",
            message="Select which command to execute",
            choices=commandNames,
        ),
    ]

    answers = inquirer.prompt(questions)

    for i in range(len(app.registered_commands)):
        if answers["value"] == app.registered_commands[i].name:
            app.registered_commands[i].callback()


if __name__ == "__main__":
    app()
