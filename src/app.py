"""Redirect shim for the retired Dash app.

The Rural AV Readiness tool now lives as a static page on the lab's GitHub Pages
site. This tiny Flask app keeps the old Render address alive and forwards every
request to the new location. Render runs it with `gunicorn --chdir src app:server`,
so the WSGI callable must be named `server`.
"""
from flask import Flask, redirect

app = Flask(__name__)
server = app  # gunicorn entry point: app:server

NEW_URL = "https://venktesh22.github.io/dashboards/Rural_AV_Readiness_Dashboard/Rural_AV_Readiness_Dashboard.html"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def moved(path):
    # 301 = moved permanently. Any path on the old host forwards to the new page.
    return redirect(NEW_URL, code=301)
