import os
import boto3
import uuid

from flask import Flask, render_template, request, url_for, redirect
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
usersTable = dynamodb.Table("Users")
tasksTable = dynamodb.Table("Tasks")

loggedIn = False
user = ""

@app.route('/')
def index():
    return render_template('index.html', loggedIn=loggedIn, user=user)

@app.route('/features')
def features():
    return render_template('features.html', loggedIn=loggedIn, user=user)

@app.route('/login', methods=["GET", "POST"])
def login():
    loginFeedback = "DNE"
    global loggedIn, user

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        response = usersTable.get_item(Key={"username": username})
        if "Item" in response:
            storedPassword = response["Item"]["password"]
            if password == storedPassword:
                loggedIn = True
                user = username
                return redirect(url_for("index"))
            else:
                loginFeedback = "passwordDNE"
        else:
            loginFeedback = "userDNE"

    return render_template('login.html', loginFeedback=loginFeedback)

@app.route('/signUp', methods=["GET", "POST"])
def signUp():
    accountStatus = "DNE"

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        response = usersTable.get_item(Key={"username": username})

        if "Item" in response:
            return render_template("signup.html", accountStatus="Exists")

        usersTable.put_item(
             Item={
                "username": username,
                "email": email,
                "password": password
             }
        )
        accountStatus = "Created"

    return render_template('signUp.html', accountStatus=accountStatus)

@app.route('/clock')
def clock():
    return render_template('clock.html', loggedIn=loggedIn, user=user)

@app.route('/edit', methods=["GET", "POST", "DELETE"])
def edit():
    global loggedIn, user

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        startTime = request.form["startTime"]
        endTime = request.form["endTime"]

        tasksTable.put_item(
             Item={
                "ID": str(uuid.uuid4()),
                "user": user,
                "title": title,
                "description": description,
                "startTime": str(startTime),
                "endTime": str(endTime)
             }
        )
    
    response = tasksTable.query(
        IndexName="user-index",
        KeyConditionExpression=Key("user").eq(user)
    )

    tasks = response.get("Items", [])
    return render_template('edit.html', loggedIn=loggedIn, user=user, taskList=tasks)

@app.route('/delete', methods=["POST"])
def delete():
    taskID = request.form["taskID"]
    
    tasksTable.delete_item(
        Key={
            'ID': taskID
        }
    )

    return redirect(url_for("edit"))

if __name__ == '__main__':
    app.run(debug=True)
