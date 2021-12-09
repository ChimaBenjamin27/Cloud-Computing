from flask_sqlalchemy import SQLAlchemy
from flask import app
from datetime import datetime

db = SQLAlchemy()

# in an interactive python shell, need to run:
# from main import db
# db.create_all()
# this will create the todo table on the db
class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


## Create extra helper methods here to interact with the database