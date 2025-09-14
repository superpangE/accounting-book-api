from datetime import datetime
from config.database import db

class Alarm(db.Model):
    __bind_key__ = 'alarm_db'
    __tablename__ = 'alarms'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    alert_at = db.Column(db.DateTime, nullable=False)
    schedule_id = db.Column(db.Integer, nullable=False, unique=True) # Link to SharedSchedule
    notify_one_hour_before = db.Column(db.Boolean, default=False, nullable=False)
    notify_one_day_before = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Alarm {self.id}: {self.message}>'

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'alert_at': self.alert_at.isoformat(),
            'schedule_id': self.schedule_id,
            'notify_one_hour_before': self.notify_one_hour_before,
            'notify_one_day_before': self.notify_one_day_before
        }