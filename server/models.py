from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cur(db.Model):
    __tablename__ = "cur"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cur_parameter = db.relationship("CurParameter", backref=db.backref("cur"))

class CurParameter(db.Model):
    __tablename__ = "cur_parameter"
    id = db.Column(db.Integer, primary_key=True)
    cur_id = db.Column(db.Integer, db.ForeignKey("cur.id"))
    name = db.Column(db.String(255), nullable=False)
    cur_parameter_value = db.relationship("CurParameterValue", backref=db.backref("Cur_parameter"))

class CurParameterValue(db.Model):
    __tablename__ = 'cur_parameter_value'
    id = db.Column(db.Integer, primary_key=True)
    cur_parameter_id = db.Column(db.Integer, db.ForeignKey('cur_parameter.id'))
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
