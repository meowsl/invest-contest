import os, re
from collections import defaultdict
from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from models import *
from fill_db import fill_db
from services import (
    CURManager,
    ModelExecute
)


# -- Конфигурация --
app = Flask(__name__, static_url_path="/static")
app.config.from_pyfile(f"{os.getcwd()}/server/config.py")
db.init_app(app)

def init_db():
    if not os.path.exists(f"{os.getcwd()}/instance/{app.config['DATABASE_FILE']}"):
        with app.app_context():
            db.create_all()
            fill_db()

def get_prediction_data():
    data = request.get_json(force=True)
    indicators = data.get('indicators')

    if indicators:
        sended_data = []
        for item in indicators:

            target_cur = db.session.query(cur_indicator).filter_by(indicator_id=int(item)).first()[0]

            indicator_values = IndicatorValue.query.filter_by(indicator_id=int(item)).all()

            target_values = [float(item.value) for item in indicator_values]

            executer = ModelExecute(target_cur, int(item), target_values)
            response = executer.process()

            years = [int(item.year) for item in indicator_values]
            years.append(2023)
            interim = {
                "cur_id": target_cur,
                "indicator_id": int(item),
                "values": response,
                "years": years
            }
            sended_data.append(interim)
        return jsonify({"data": sended_data}), 200
    else:
        return jsonify({"status": "error"}), 500

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/predict', methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        return get_prediction_data()

    list_cur = [{
        "name": item.name,
        "id": item.id
    } for item in Cur.query.all()]

    list_indicators = [{
        "name": re.sub(r'\W+', ' ', item.name),
        "indicator_id": item.id,
    } for item in Indicator.query.all()]

    check_list = []

    result = defaultdict(list)

    for cur_id, indicator_id in db.session.query(cur_indicator).all():
        result[cur_id].append(indicator_id)

    test = [{"cur_id": cur_id, "indicator_id": indicator_ids} for cur_id, indicator_ids in result.items()]

    return render_template("predict.html", list_cur=list_cur, list_indicators=list_indicators, check_data=test)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

if __name__ == "__main__":
    init_db()
    app.run("0.0.0.0", port=8000, debug=True)
