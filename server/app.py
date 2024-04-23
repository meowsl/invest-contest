from flask import (
    Flask,
    render_template
)
from flask_sqlalchemy import SQLAlchemy
import os

# -- Конфигурация --
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile(f'{os.getcwd()}/server/config.py')
db = SQLAlchemy()
db.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run('0.0.0.0', port=8000, debug=True)