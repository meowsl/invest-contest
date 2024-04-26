from models import *
from services import (
    CURManager,
    ExcelParser
)

def fill_db():
    '''
    Заполнение БД исходя из файла
    '''
    parser = ExcelParser("train_models/data/data.xlsx")
    data = parser.find_rows_by_first_cell_value("Ростовская область")

    cur_manager = CURManager()

    for cur in cur_manager.CUR_NAMES.keys():
        new_cur = Cur(
            name=cur_manager.CUR_NAMES[cur]
        )
        db.session.add(new_cur)
        db.session.commit()

    for item in data:
        # Определяем название ЦУРа
        target_cur = None
        for number, array in cur_manager.DATA_CUR.items():
            if str(item["Indicator"]) in array:
                target_cur = number
                break

        # Создаем новый индикатор
        new_indicator = Indicator(
            name=item['Name'],
            number=item['Indicator']
        )
        db.session.add(new_indicator)
        db.session.commit()

        name_cur = cur_manager.CUR_NAMES[target_cur]
        checked_cur = Cur.query.filter_by(name=name_cur).first()
        checked_cur.indicator.append(new_indicator)
        db.session.commit()

        for i in range(len(item['Years'])):
            new_value = IndicatorValue(
                year=item['Years'][i],
                value=item['Values'][i],
                indicator_id = new_indicator.id
            )
            db.session.add(new_value)
            db.session.commit()