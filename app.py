
"""

"""

# run this file ----->
from website import create_app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host= '192.168.1.243')

from flask import Flask, render_template, request, redirect
from flask import *
from flask_recaptcha import ReCaptcha
from flask_wtf import RecaptchaField
import sqlite3

app = Flask(__name__)
db_locale = 'students.db'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf2mcMhAAAAAHPekK8_exQ5enP1db6kYKlevRyb'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf2mcMhAAAAALsvyxebf4_d8gSHDE5ZkYa3hNpo'
recaptcha = ReCaptcha(app)


@app.route('/')
@app.route('/home')
def home_page():
    student_data = query_contact_details()
    return render_template('home.html', student_data=student_data)

@app.route('/add')
def add_student():
    return 'Here is where we add students'

def query_contact_details():
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    c.execute("""
    SELECT * FROM contact
    """)
    student_data = c.fetchall()
    return student_data

@app.route('/add', methods = ["GET", "POST"])
def check_input():
    if request.method == "POST":
        form = request.form
        question1 = int(form("question1"))
        question1 = int(form("question1"))



if __name__ == '__main__':
    app.run()

