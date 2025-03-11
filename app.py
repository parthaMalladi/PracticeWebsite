import os
import boto3
import uuid

from flask import Flask, render_template, request, url_for

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

@app.route('/login')
def login():
    return render_template('login.html', loggedIn=loggedIn, user=user)

@app.route('/signUp')
def signUp():
    return render_template('signUp.html', loggedIn=loggedIn, user=user)

@app.route('/clock')
def clock():
    return render_template('clock.html', loggedIn=loggedIn, user=user)

@app.route('/edit')
def edit():
    return render_template('edit.html', loggedIn=loggedIn, user=user)

if __name__ == '__main__':
    app.run(debug=True)
