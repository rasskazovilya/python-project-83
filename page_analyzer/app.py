import os
from urllib.parse import urlparse

import psycopg2
import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from page_analyzer import db

from .url_validator import validate

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/")
def index():
    return render_template(
        'index.html'
    )


@app.get("/urls")
def get_sites():
    urls = db.get_urls(conn)

    return render_template(
        'url_table.html',
        urls=urls
    )


@app.post("/urls")
def add_site():
    url = request.form.get("url")

    errors = validate(url)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html', code=422)

    parsed_url = urlparse(url)
    root_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    id = db.add_url(conn, root_url)

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for("get_site", id=id), code=302)


@app.get("/urls/<id>")
def get_site(id):
    url = db.get_url(conn, id)
    checks = db.get_url_checks(conn, id)

    return render_template(
        'url.html',
        url=url,
        checks=checks
    )


@app.post("/urls/<id>/checks")
def check_site(id):
    url = db.get_url(conn, id)
    try:
        response = requests.get(url['name'])
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for("get_site", id=id))
    # perform_check(url)
    db.add_check(
        conn,
        id,
        response.status_code,
        h1='',
        title='',
        desc=''
    )

    flash('Страница успешно проверена', 'success')
    return redirect(url_for("get_site", id=id))
