from datetime import datetime, date
from config.database import db

class AccountingBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False) # Added user_id column
    card = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    person = db.Column(db.String(80), nullable=False)

    is_send = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<AccountingBook {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id, # Added user_id to dict
            'card': self.card,
            'date': self.date.isoformat(),
            'amount': self.amount,
            'detail': self.detail,
            'category': self.category,
            'person': self.person,
            'is_send': self.is_send
        }
