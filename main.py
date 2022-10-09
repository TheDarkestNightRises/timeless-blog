from flask import Flask
from flask import render_template
from flask import request
from email.message import EmailMessage
import config
import requests
import smtplib

response = requests.get(url=config.API)
response.raise_for_status()
data = response.json()
print(data)
app = Flask(__name__)
my_email = config.EMAIL_ADDRESS
password = config.EMAIL_PASSWORD


@app.route('/')
def home_page():
    return render_template('index.html', data=data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post.html')
def post():
    return render_template('post.html')


@app.route('/<int:index>')
def show_page(index):
    requested_data_post = None
    for i in range(len(data) + 1):
        if index == i:
            requested_data_post = data[i - 1]
    return render_template('post.html', data=requested_data_post)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/contact', methods=['POST', 'GET'])
def receive_data():
    if request.method == 'GET':
        msg_sent = False
    else:
        name = request.form['name']
        email = request.form['email']
        telephone = request.form['phone']
        body = request.form['message']
        msg_sent = True
        message = EmailMessage()
        message["Subject"] = 'New Message'
        message["From"] = my_email
        message["To"] = config.CONTACT_EMAIL
        body = f"Name:{name} \n Email:{email} \n Telephone:{telephone} \n {body}"
        message.set_content(body)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(my_email, password=password)
            connection.send_message(message)
        name = None
        email = None
        body = None
        telephone = None

    return render_template('contact.html', msg_sent=msg_sent)


if __name__ == '__main__':
    app.run(debug=True)
