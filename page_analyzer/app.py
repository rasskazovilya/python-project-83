import os
from urllib.parse import urlparse

import psycopg2
import requests
import bs4
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from page_analyzer import db

from .url_validator import validate

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/")
def index():
    return render_template(
        'index.html'
    )


@app.get("/urls")
def get_urls():
    with psycopg2.connect(DATABASE_URL) as conn:
        urls = db.get_urls(conn)

    return render_template(
        'url_table.html',
        urls=urls
    )


@app.post("/urls")
def add_url():
    url = request.form.get("url")

    errors = validate(url)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html'), 422

    parsed_url = urlparse(url)
    root_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    with psycopg2.connect(DATABASE_URL) as conn:
        exist_url = db.get_url(conn, cond='name', value=root_url)
    if exist_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for("get_url", id=exist_url['id']), code=302)

    with psycopg2.connect(DATABASE_URL) as conn:
        id = db.add_url(conn, root_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for("get_url", id=id), code=302)


@app.get("/urls/<id>")
def get_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        url = db.get_url(conn, cond='id', value=id)
        checks = db.get_url_checks(conn, id)

    return render_template(
        'url.html',
        url=url,
        checks=checks
    )


@app.post("/urls/<id>/checks")
def check_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        url = db.get_url(conn, cond='id', value=id)
        print(url)
    try:
        response = requests.get(url['name'])
        response.raise_for_status()
        if response.status_code != 200:
            raise requests.RequestException
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for("get_url", id=id))

    bs = bs4.BeautifulSoup(response.text, 'html.parser')
    h1 = bs.h1.string if bs.h1 else ''
    title = bs.title.string if bs.title else ''
    desc_tag = bs.find('meta', attrs={'name': 'description'})
    desc = desc_tag.get('content') if desc_tag else ''

    with psycopg2.connect(DATABASE_URL) as conn:
        db.add_check(
            conn,
            id,
            response.status_code,
            h1=h1,
            title=title,
            desc=desc
        )

    flash('Страница успешно проверена', 'success')
    return redirect(url_for("get_url", id=id))
