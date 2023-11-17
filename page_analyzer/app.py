import os
import datetime
from urllib.parse import urlparse

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/")
def hello_world():
    return render_template(
        'index.html'
    )


@app.get("/urls")
def get_sites():
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        select_all_query = "SELECT * FROM urls ORDER BY created_at DESC;"
        curs.execute(select_all_query)
        urls = curs.fetchall()

    return render_template(
        'url_table.html',
        urls=urls
    )


@app.post("/urls")
def add_site():
    url = request.form.get("url")
    errors = urlparse(url)

    with conn.cursor() as curs:
        created_at = datetime.datetime.today()
        insert_query = """
        INSERT INTO urls (name, created_at)
        VALUES (%s, %s) RETURNING id;
        """
        curs.execute(insert_query, (url, created_at))
        conn.commit()
        id = curs.fetchone()[0]
        print(id)

    return redirect(url_for("get_site", id=id), code=302)


@app.get("/urls/<id>")
def get_site(id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        select_id_query = "SELECT * FROM urls WHERE id=%s;"
        curs.execute(select_id_query, (id,))
        url = curs.fetchone()
    if request.method == "POST":
        flash('Страница успешно добавлена', 'success')
    return render_template(
        'url.html',
        url=url
    )
