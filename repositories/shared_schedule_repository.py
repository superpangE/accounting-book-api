from config.database import db
from models.shared_schedule import SharedSchedule
from datetime import datetime

class SharedScheduleRepository:
    def create(self, user_id, data):
        new_schedule = SharedSchedule(
            user_id=user_id,
            person=data['person'],
            description=data['description'],
            date=datetime.fromisoformat(data['date']),
            notify_one_hour_before=data.get('notify_one_hour_before', False),
            notify_one_day_before=data.get('notify_one_day_before', False)
        )
        db.session.add(new_schedule)
        db.session.commit()
        return new_schedule

    def get_all(self, user_id, start_date=None, end_date=None):
        query = SharedSchedule.query.filter_by(user_id=user_id)
        if start_date:
            query = query.filter(SharedSchedule.date >= start_date)
        if end_date:
            query = query.filter(SharedSchedule.date <= end_date)
        return query.all()

    def get_by_id(self, user_id, id):
        return SharedSchedule.query.filter_by(user_id=user_id, id=id).first()

    def update(self, user_id, schedule, data):
        # Ensure the schedule belongs to the user before updating
        if schedule.user_id != user_id:
            return None # Or raise an exception for unauthorized access
        schedule.person = data.get('person', schedule.person)
        schedule.description = data.get('description', schedule.description)
        schedule.date = datetime.fromisoformat(data.get('date', schedule.date.isoformat()))
        schedule.notify_one_hour_before = data.get('notify_one_hour_before', schedule.notify_one_hour_before)
        schedule.notify_one_day_before = data.get('notify_one_day_before', schedule.notify_one_day_before)
        db.session.commit()
        return schedule

    def delete(self, user_id, schedule):
        # Ensure the schedule belongs to the user before deleting
        if schedule.user_id != user_id:
            return False # Or raise an exception for unauthorized access
        db.session.delete(schedule)
        db.session.commit()

    def get_schedules_by_user_id(self, user_id):
        return SharedSchedule.query.filter_by(user_id=user_id).all()