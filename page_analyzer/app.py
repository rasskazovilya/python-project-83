import os
import datetime
from urllib.parse import urlparse

import psycopg2
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route("/")
def hello_world():
    return render_template(
        'index.html'
    )


@app.post("/urls")
def add_site():
    url = request.form.get("url")
    errors = urlparse(url)
    with conn.cursor() as curs:
        created_at = datetime.datetime.today()
        insert_query = "INSERT INTO urls (name, created_at) VALUES (%s, %s)"
        print(curs.mogrify(insert_query, (url, created_at)))
        curs.execute(insert_query, (url, created_at))
        

    return redirect("/urls", code=302)
