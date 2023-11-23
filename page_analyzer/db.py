import datetime
import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_urls():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            select_all_query = """
            SELECT urls.id,
                name,
                MAX(url_checks.created_at) AS last_date,
                status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id, status_code
            ORDER BY urls.id DESC;
            """
            curs.execute(select_all_query)
            urls = curs.fetchall()
    return urls


def add_url(url):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            created_at = datetime.datetime.today().replace(microsecond=0)
            insert_query = """
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s) RETURNING id;
            """
            curs.execute(insert_query, (url, created_at))
            conn.commit()
            id = curs.fetchone()[0]
    return id


def get_url(cond, value):
    conditions = {"name": "WHERE name=%s;", "id": "WHERE id=%s;"}
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            select_name_query = "SELECT * FROM urls " + conditions[cond]
            curs.execute(select_name_query, (value,))
            url = curs.fetchone()
    return url


def get_url_checks(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            select_checks_query = """
            SELECT * FROM url_checks
            WHERE url_id=%s
            ORDER BY created_at DESC;
            """
            curs.execute(select_checks_query, (url_id,))
            checks = curs.fetchall()
    return checks


def add_check(url_id, status_code, h1, title, desc):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            created_at = datetime.datetime.today().replace(microsecond=0)

            add_check_query = """
            INSERT INTO url_checks (
                url_id,
                status_code,
                h1,
                title,
                description,
                created_at
            ) VALUES (%s, %s, %s, %s, %s, %s);
            """
            curs.execute(
                add_check_query,
                (url_id, status_code, h1, title, desc, created_at)
            )
            conn.commit()
    return
