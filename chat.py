from flask import Flask, render_template, request
import json
import random
import re




import pymysql


import torch


from model import NeuralNet


from nltk_utils import bag_of_words, tokenize


from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get')
def chatbot_response():
    message = request.args.get('msg')
    return get_response(message)

def get_response(message):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="kormaz88",
        database="employees",
    )
    mycursor = mydb.cursor()


    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)

    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    bot_name = "TFG"

    def get_employee_info(emp_no):
        mycursor.execute(f"SELECT first_name FROM employees.employees WHERE emp_no = {emp_no}")
        result = mycursor.fetchone()
        if result:
            return result[0]
        else:
         return None

    def get_employee_hire_date(first_name, last_name):
         mycursor.execute(f"SELECT hire_date FROM employees.employees WHERE first_name = %s AND last_name = %s",
                             (first_name, last_name))
         result = mycursor.fetchone()
         if result:
            return result[0]
         else:
             return None

    def get_department_info(dept_no):
        mycursor.execute(f"SELECT dept_name FROM employees.departments WHERE dept_no = %s", (dept_no,))
        result = mycursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_employee_title(emp_no):
        mycursor.execute(f"SELECT title FROM employees.titles WHERE emp_no = {emp_no} ")
        result = mycursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_employee_salary(emp_no):
        mycursor.execute(f"SELECT salary FROM employees.salaries WHERE emp_no = {emp_no} ")
        result = mycursor.fetchone()
        if result:
            return result[0]
        else:
            return None





    sentence = message
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    prob = torch.softmax(output, dim=1)[0][predicted.item()]
    if prob.item() > 0.5:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if tag == "employee_info":
                    pattern = re.compile(r'employee\s+(\d+)', re.IGNORECASE)
                    match = pattern.search(" ".join(sentence))
                    if match:
                        emp_no = match.group(1)
                        first_name = get_employee_info(emp_no)
                        if first_name is not None:
                            response = intent['responses'][0].format(emp_no=emp_no, first_name=first_name)
                        else:
                            response = "I couldn't find that employee's information."
                    else:
                        response = "Please provide an employee number."
                elif tag == "employee_hire_date":
                    pattern = re.compile(r'(\w+)\s+(\w+)\s+hired?', re.IGNORECASE)
                    match = pattern.search(" ".join(sentence))
                    if match:
                        first_name, last_name = match.group(1), match.group(2)
                        hire_date = get_employee_hire_date(first_name, last_name)
                        if hire_date is not None:
                            response = intent['responses'][0].format(first_name=first_name, last_name=last_name,
                                                                     hire_date=hire_date)
                        else:
                            response = "I couldn't find that employee's information."
                    else:
                        response = "Please provide the first and last name of the employee."
                elif tag == "department_info":
                    pattern = re.compile(r'department\s+(d\d{3})', re.IGNORECASE)
                    match = pattern.search(" ".join(sentence))
                    if match:
                        dept_no = match.group(1)
                        dept_name = get_department_info(dept_no)
                        if dept_name is not None:
                            response = intent['responses'][0].format(dept_no=dept_no, dept_name=dept_name)
                        else:
                            response = "I couldn't find that department's information."
                    else:
                        response = "Please provide a department number."
                elif tag == "employee_title":
                    pattern = re.compile(r'employee\s+(\d+)', re.IGNORECASE)
                    match = pattern.search(" ".join(sentence))
                    if match:
                        emp_no = match.group(1)
                        title = get_employee_title(emp_no)
                        if title is not None:
                            response = intent['responses'][0].format(emp_no=emp_no, title=title)
                        else:
                            response = "I couldn't find that employee's title information."
                    else:
                        response = "Please provide an employee number."


                elif tag == "employee_salary":
                    pattern = re.compile(r'employee\s+(\d+)', re.IGNORECASE)
                    match = pattern.search(" ".join(sentence))
                    if match:
                        emp_no = match.group(1)
                        salary = get_employee_salary(emp_no)
                        if salary is not None:
                            response = intent['responses'][0].format(emp_no=emp_no, salary=salary)
                        else:
                            response = "I couldn't find that employee's salary information."
                    else:
                        response = "Please provide an employee number."

                else:
                    response = random.choice(intent['responses'])
                return f"{bot_name}: {response}"
    else:
        return f"{bot_name}: I do not understand..."


if __name__ == '__main__':
    app.run(debug=True)