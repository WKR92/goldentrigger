from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint, flash, session, jsonify, current_app
from forms import UploadPDFForm
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
import re
from pdfminer.high_level import extract_text
from queue import Empty, Queue
from apscheduler.schedulers.blocking import BlockingScheduler
from flask_apscheduler import APScheduler
import json
import threading
import time
import concurrent.futures
import atexit
from flask_session import Session
import redis



db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    # db = SQLAlchemy(app)
    db.init_app(app)
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    SESSION_REDIS = redis.from_url('redis://127.0.0.1:6379')
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_MODIFIED"] = True
    Session(app)
    return app


app = create_app()
app.app_context().push()
sess = Session(app)


global raw_text
raw_text = []
global split_text
split_text = []
global firstCut
firstCut = []
global secondCut
secondCut = []
global thirdCutList
thirdCutList = []
global data
data = []


def save_pdf(pdf_form):
    # random_hex = secrets.token_hex(8)
    f_namee, f_ext = os.path.splitext(pdf_form.filename)
    pdf_fn = f_namee + f_ext
    pdf_path = os.path.join(app.root_path, 'static/user_pdf', pdf_fn)
    pdf_form.save(pdf_path)

    return pdf_path


def tittle_of_book(pdf_path):
    parts = []
    path = pdf_path
    cut = path.split("\\")
    parts.append(cut)
    tittle = parts[0][-1]
    ready_tittle = tittle[:-4]
    ready_tittle_pretty_cut = ready_tittle.replace("_", " ")
    pretty_tittle = ready_tittle_pretty_cut.replace("  ", " ")
    return pretty_tittle


def convert_pdf_to_txt(path):
    text = extract_text(path)
    raw_text.append(text)


def split(lista):
    for i in lista:
        split = i.split(" ")
        split_text.append(split)


def first_text_clean(lista):
    for i in lista[0]:
        if "\n" in i:
            cut = i.replace('\n', ' ')
            firstCut.append(cut)
        elif i == "\n":
            continue
        else:
            firstCut.append(i)


def second_text_clean(lista):
    for i in lista:
        if re.search(r"(\s)", i, re.I):
            cut = re.split(r"(\s)", i)
            for j in cut:
                secondCut.append(j)
        else:
            secondCut.append(i)


def third_text_clean(lista):
    for i in lista:
        if re.match(r"(\s)", i):
            continue
        elif i == '':
            continue
        else:
            thirdCutList.append(i)


def clearLists():
    global raw_text
    raw_text = []
    global split_text
    split_text = []
    global firstCut
    firstCut = []
    global secondCut
    secondCut = []
    global thirdCutList
    thirdCutList = []
    global data
    data = []



@app.route('/', methods=['GET', 'POST', 'PUT'])
@app.route('/home', methods=['GET', 'POST','PUT'])
def home():
    print(request.path)
    form = UploadPDFForm()
    if form.validate_on_submit():
        if form.pdfFile.data:
            pdf_file = save_pdf(form.pdfFile.data)
            print(pdf_file)
            session['my_var'] = pdf_file

            # Poniższa funkcja oczyszcza listy przed załadowaniem do nich nowego tekstu
            clearLists()
            
        
        return redirect(url_for('reader'))
            

    return render_template('home.html', title='Upload page', form=form)



@app.route('/about', methods=['GET', 'POST', 'PUT'])
def about():
    return render_template('about.html', title='About')


@app.route('/loadReader', methods=['GET', 'POST', 'PUT'])
def loadReader():
    bookTittle = ""
    data = []
    return render_template('loadReader.html', title='Web_Reader', data=json.dumps(data), bookTitle = json.dumps(bookTittle))


@app.route('/reader', methods=['GET', 'POST', 'PUT'])
def reader():
    print(request.path)
    my_var = session.get('my_var', None)
    bookTittle = tittle_of_book(my_var)
    convert_pdf_to_txt(my_var)
    split(raw_text)
    first_text_clean(split_text)
    second_text_clean(firstCut)
    third_text_clean(secondCut)
    data = thirdCutList
    flash('Your file is uploaded. Have a nice read.', "success")

    return render_template('reader.html', title='Web Reader', data=json.dumps(data), bookTitle = json.dumps(bookTittle))


if __name__ == "__main__":
    app.run(debug=True)
