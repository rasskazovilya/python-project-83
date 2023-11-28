import datetime
import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_checks():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            select_all_url_checks_query = """
            SELECT url_id, created_at, status_code
            FROM url_checks
            ORDER BY created_at DESC;
            """
            curs.execute(select_all_url_checks_query)
            url_checks = curs.fetchall()
    return url_checks


def get_urls():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            select_all_url_id_query = """
            SELECT id, name FROM urls
            ORDER BY id DESC;
            """
            curs.execute(select_all_url_id_query)
            urls = curs.fetchall()
    return urls


def get_urls_and_checks():
    url_names = get_urls()
    checks = get_checks()

    urls = []
    for url in url_names:
        url_id = url["id"]
        check = next(
            (check for check in checks if check["url_id"] == url_id), dict()
        )
        urls.append(
            {
                "id": url_id,
                "name": url["name"],
                "last_date": check.get("created_at", None),
                "status_code": check.get("status_code", None),
            }
        )
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
                (url_id, status_code, h1, title, desc, created_at),
            )
            conn.commit()
    return
