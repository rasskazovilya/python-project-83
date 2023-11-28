import datetime
import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_all(table):
    queries = {
        "urls": "SELECT * FROM urls;",
        "url_checks": "SELECT * FROM url_checks;",
    }
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            curs.execute(queries[table])
            results = curs.fetchall()
    return results


def get_urls_and_checks():
    url_names = get_all("urls")
    url_names.sort(key=lambda x: x["id"], reverse=True)
    checks = get_all("url_checks")
    checks.sort(key=lambda x: x["created_at"], reverse=True)

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


def add_check(url_id, status_code, seo_data):
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
                (
                    url_id,
                    status_code,
                    seo_data["h1"],
                    seo_data["title"],
                    seo_data["desc"],
                    created_at,
                ),
            )
            conn.commit()
    return
