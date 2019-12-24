from myproject import app
from flask import render_template, Response


@app.errorhandler(404)
def not_found(e):
    resp = Response(render_template('404.html'), status=404)
    return resp