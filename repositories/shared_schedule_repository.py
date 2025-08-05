from config.database import db
from models.shared_schedule import SharedSchedule
from datetime import datetime

class SharedScheduleRepository:
    def create(self, data):
        new_schedule = SharedSchedule(
            person=data['person'],
            description=data['description'],
            date=datetime.fromisoformat(data['date'])
        )
        db.session.add(new_schedule)
        db.session.commit()
        return new_schedule

    def get_all(self):
        return SharedSchedule.query.all()

    def get_by_id(self, id):
        return SharedSchedule.query.get(id)

    def update(self, schedule, data):
        schedule.person = data.get('person', schedule.person)
        schedule.description = data.get('description', schedule.description)
        schedule.date = datetime.fromisoformat(data.get('date', schedule.date.isoformat()))
        db.session.commit()
        return schedule

    def delete(self, schedule):
        db.session.delete(schedule)
        db.session.commit()