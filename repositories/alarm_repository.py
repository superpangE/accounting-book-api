from config.database import db
from models.alarm import Alarm
from datetime import datetime

class AlarmRepository:
    def create(self, data):
        new_alarm = Alarm(
            message=data['message'],
            alert_at=datetime.fromisoformat(data['alert_at']),
            schedule_id=data['schedule_id'],
            notify_one_hour_before=data.get('notify_one_hour_before', False),
            notify_one_day_before=data.get('notify_one_day_before', False)
        )
        db.session.add(new_alarm)
        db.session.commit()
        return new_alarm

    def get_by_schedule_id(self, schedule_id):
        return Alarm.query.filter_by(schedule_id=schedule_id).first()

    def update(self, alarm, data):
        alarm.message = data.get('message', alarm.message)
        alarm.alert_at = datetime.fromisoformat(data.get('alert_at', alarm.alert_at.isoformat()))
        alarm.notify_one_hour_before = data.get('notify_one_hour_before', alarm.notify_one_hour_before)
        alarm.notify_one_day_before = data.get('notify_one_day_before', alarm.notify_one_day_before)
        db.session.commit()
        return alarm

    def delete(self, alarm):
        db.session.delete(alarm)
        db.session.commit()