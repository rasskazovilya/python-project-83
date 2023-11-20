import os
import datetime
from urllib.parse import urlparse
from .url_validator import validate

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
def index():
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

    errors = validate(url)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html', code=422)

    parsed_url = urlparse(url)
    root_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    with conn.cursor() as curs:
        created_at = datetime.datetime.today().replace(microsecond=0)
        insert_query = """
        INSERT INTO urls (name, created_at)
        VALUES (%s, %s) RETURNING id;
        """
        curs.execute(insert_query, (root_url, created_at))
        conn.commit()
        id = curs.fetchone()[0]

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for("get_site", id=id), code=302)


@app.get("/urls/<id>")
def get_site(id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        select_id_query = "SELECT * FROM urls WHERE id=%s;"
        curs.execute(select_id_query, (id,))
        url = curs.fetchone()

        select_checks_query = """
        SELECT * FROM url_checks
        WHERE url_id=%s
        ORDER BY created_at DESC;
        """
        curs.execute(select_checks_query, (id,))
        checks = curs.fetchall()

    return render_template(
        'url.html',
        url=url,
        checks=checks
    )


@app.post("/urls/<id>/checks")
def check_site(id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        created_at = datetime.datetime.today().replace(microsecond=0)

        add_check = """
        INSERT INTO url_checks (
            url_id,
            status_code,
            h1,
            title,
            description,
            created_at
        ) VALUES (%s, %s, %s, %s, %s, %s);
        """
        curs.execute(add_check, (id, 200, '', '', '', created_at))
        conn.commit()

    flash('Страница успешно проверена', 'success')
    return redirect(url_for("get_site", id=id), code=302)
