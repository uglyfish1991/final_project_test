from . import db 

class Salesfigures(db.Model):
    # the variable id is a column of a unique int, used to look up users
    id = db.Column(db.Integer, primary_key = True)
    money_made = db.Column(db.Integer(), nullable=False)
    biggest_spend = db.Column(db.Integer(),nullable=False)
    bestseller = db.Column(db.String(40),nullable=False)
    worstseller = db.Column(db.String(40),nullable=False)
    mvp = db.Column(db.String(40),nullable=False)
    