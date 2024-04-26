from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import(
    Mapped,
    mapped_column
)
from sqlalchemy import (
    String,
    Integer,
    Numeric,
    ForeignKey,
    CheckConstraint
)

db = SQLAlchemy()

cur_indicator = db.Table(
    "cur_indicator",
    db.Column("cur_id", Integer(), ForeignKey("cur.id")),
    db.Column("indicator_id", Integer(), ForeignKey("indicator.id"))
)

class Cur(db.Model):
    __tablename__ = "cur"
    '''
    Модель ЦУРов
    '''
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), info={"label": "Полное название цели"})
    indicator = db.relationship("Indicator", secondary="cur_indicator",
                                backref=db.backref("indicators", lazy="dynamic"),
                                info={"label":"Показатели"})

class Indicator(db.Model):
    __tablename__ = "indicator"
    '''
    Показатели ЦУРов
    '''
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), info={"label":"Название"})
    number: Mapped[str] = mapped_column(String(8), info={"label":"Номер индикатора по листу"})

class IndicatorValue(db.Model):
    __tablename__ = "indicator_value"
    '''
    Значения показателей
    '''
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer, info={"label": "Год"})
    month: Mapped[int] = mapped_column(Integer, CheckConstraint('month >= 1 and month <= 12'), nullable=True, info={"label": "Месяц"})
    value: Mapped[float] = mapped_column(Numeric(precision=15, scale=2), info={"label": "Значение"})
    indicator_id: Mapped[int] = mapped_column(Integer, ForeignKey("indicator.id"), info={"label": "ID показателя"})

    @staticmethod
    def validate_month(month):
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12")