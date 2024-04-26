from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from models import *
from fill_db import fill_db
from services import CURManager, ModelExecute
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
    '''
    вот эта вся залупа отвечает за обработку пост запроса.
    '''
    if request.method == "POST":
        # здесь мы получаем жсон просто с фронта ниче особенного
        data = request.get_json()
        indicators = data.get('indicators')

        # Валидация на пустое значение
        if indicators:
            sended_data = [] # массив для того, чтобы отправить его потом обратно и радоваться жизни

            # тут как я говорил мы через цикл перебираем все выбранные показатели
            for item in indicators:

                target_cur = db.session.query(cur_indicator).filter_by(indicator_id=int(item)).first()[0] # Это отправляем в сервис || короче вот здесь мы получаем из бдшки айди цура

                indicator_values = IndicatorValue.query.filter_by(indicator_id=int(item)).all()
                target_values = [float(item.value) for item in indicator_values] # Это отправляем в сервис || дальше здесь мы получаем все значения (они оказывается сами фильтруются по годам) и заносим их в массив

                executer = ModelExecute(target_cur, int(item), target_values) # здесь самое интересное. по сути мы вызываем класс (сервис) и передаем туда переменные для инициализации

                response = executer.process() # здесь мы уже вызываем непосредственно логическую функцию, которая нам запускает модель и вкидывает туда массив который мы ей предоставили. дальше переходим в сервис

                # после того как мы в переменную response получили данные, засовываем так же в теле цикла в словарь промежуточный
                interim = {
                    "cur_id": target_cur,
                    "indicator_id": int(item),
                    "values": response
                }

                print(interim)
                sended_data.append(interim) # а дальше просто добавляем в массив, который в дальнейшем отправим на фронт обратно

            return jsonify({"data":sended_data}), 200
        else:
            return jsonify({"status":"error"}), 500

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
