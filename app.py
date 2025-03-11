import os
import boto3
import uuid

from flask import Flask, render_template, request

app = Flask(__name__)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('MyTable')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            result = num1 / num2 if num2 != 0 else "Error: Division by zero"
        else:
            result = "Invalid Operation"

        # Store in DynamoDB
        table.put_item(
            Item={
                'ID': str(uuid.uuid4()),  # Generate a unique ID
                'num1': str(num1),
                'num2': str(num2),
                'operation': operation,
                'result': str(result)
            }
        )

    except ValueError:
        result = "Invalid Input"

    return render_template('result.html', num1=num1, num2=num2, operation=operation, result=result)

if __name__ == '__main__':
    app.run(debug=True)
