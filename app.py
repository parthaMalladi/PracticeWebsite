import os
import boto3
import uuid

from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('MyTable')

loggedIn = True
user = ""

@app.route('/')
def index():
    return render_template('index.html', loggedIn=loggedIn, user=user)

if __name__ == '__main__':
    app.run(debug=True)
