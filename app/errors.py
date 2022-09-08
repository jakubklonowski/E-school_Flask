from flask import render_template

from app import app


@app.errorhandler(401)
def error401(e):
    return render_template('401.html'), 401


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404
