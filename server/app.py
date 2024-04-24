from flask import (
    Flask,
    render_template,
    request
)
from flask_sqlalchemy import SQLAlchemy
from models import db
import os

# -- Конфигурация --
app = Flask(__name__, static_url_path="/static")
app.config.from_pyfile(f"{os.getcwd()}/server/config.py")
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/predict', methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        pass

    return render_template("predict.html")


if __name__ == "__main__":
    if not os.path.exists(f"{os.getcwd()}/instance/{app.config['DATABASE_FILE']}"):
        with app.app_context():
            db.create_all()
    app.run("0.0.0.0", port=8000, debug=True)
