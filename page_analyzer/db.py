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
        insert_query = """
        INSERT INTO urls (name)
        VALUES (%s) RETURNING id;
        """
        curs.execute(insert_query, (url,))
        conn.commit()
        id = curs.fetchone()[0]
    return id


def get_url(conn, id):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        select_id_query = "SELECT * FROM urls WHERE id=%s;"
        curs.execute(select_id_query, (id,))
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
        curs.execute(
            add_check,
            (url_id, status_code, h1, title, desc, created_at)
        )
        conn.commit()