import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template(
        'index.html'
    )
