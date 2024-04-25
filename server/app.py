from flask import (
    Flask,
    render_template,
    request
)
from flask_sqlalchemy import SQLAlchemy
from models import *
from fill_db import fill_db
from services import CURManager
from collections import defaultdict
import os, re

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

    list_cur = [{
        "name": item.name,
        "id":item.id
    } for item in Cur.query.all()]

    list_indicators = [{
        "name": re.sub(r'\W+', ' ', item.name),
        "indicator_id": item.id
    } for item in Indicator.query.all()]

    check_list = []

    result = defaultdict(list)

    for cur_id, indicator_id in db.session.query(cur_indicator).all():
        result[cur_id].append(indicator_id)

    test = [{"cur_id": cur_id, "indicator_id": indicator_ids} for cur_id, indicator_ids in result.items()]

    return render_template("predict.html", list_cur=list_cur, list_indicators=list_indicators, check_data=test)


if __name__ == "__main__":
    if not os.path.exists(f"{os.getcwd()}/instance/{app.config['DATABASE_FILE']}"):
        with app.app_context():
            db.create_all()
            fill_db()

    app.run("0.0.0.0", port=8000, debug=True)
