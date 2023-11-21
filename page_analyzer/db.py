import psycopg2
import psycopg2.extras
import datetime


def get_urls(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        select_all_query = "SELECT * FROM urls ORDER BY created_at DESC;"
        curs.execute(select_all_query)
        urls = curs.fetchall()
    return urls


def add_url(conn, url):
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


def get_url(conn, id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        select_id_query = "SELECT * FROM urls WHERE id=%s;"
        curs.execute(select_id_query, (id,))
        url = curs.fetchone()
    return url


def get_url_by_name(conn, name):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        select_name_query = "SELECT * FROM urls WHERE name=%s;"
        curs.execute(select_name_query, (name,))
        url = curs.fetchone()
    return url


def get_url_checks(conn, url_id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        select_checks_query = """
        SELECT * FROM url_checks
        WHERE url_id=%s
        ORDER BY created_at DESC;
        """
        curs.execute(select_checks_query, (url_id,))
        checks = curs.fetchall()
    return checks


def add_check(conn, url_id, status_code, h1, title, desc):
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
