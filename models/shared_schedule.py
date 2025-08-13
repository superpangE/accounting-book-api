from datetime import datetime
from config.database import db

class SharedSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False) # Added user_id column
    person = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<SharedSchedule {self.id}: {self.person} - {self.description}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id, # Added user_id to dict
            'person': self.person,
            'description': self.description,
            'date': self.date.isoformat(timespec='seconds')
        }