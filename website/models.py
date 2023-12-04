from . import db 

class Salesfigures(db.Model):
    # the variable id is a column of a unique int, used to look up users
    id = db.Column(db.Integer, primary_key = True)
    money_made = db.Column(db.Integer())
    biggest_spend = db.Column(db.Integer())
    bestseller = db.Column(db.String(40))
    worstseller = db.Column(db.String(40))
    mvp = db.Column(db.String(40))
    