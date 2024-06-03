from flask import Flask, request, render_template_string
from werkzeug.security import escape
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    safe_name = escape(name)  # Prevent XSS
    return f'Hello, {safe_name}!'

@app.errorhandler(404)
def page_not_found(e):
    return render_template_string('<h1>Page Not Found</h1>'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template_string('<h1>Internal Server Error</h1>'), 500

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')