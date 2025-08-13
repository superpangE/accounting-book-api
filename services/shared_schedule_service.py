from repositories.shared_schedule_repository import SharedScheduleRepository
from repositories.alarm_repository import AlarmRepository

class SharedScheduleService:
    def __init__(self):
        self.repository = SharedScheduleRepository()
        self.alarm_repository = AlarmRepository()

    def create_schedule(self, user_id, data):
        new_schedule = self.repository.create(user_id, data)
        # Create alarm entry
        alarm_message = f"{new_schedule.person}-{new_schedule.description}"
        alarm_data = {
            'message': alarm_message,
            'alert_at': new_schedule.date.isoformat(),
            'schedule_id': new_schedule.id
        }
        self.alarm_repository.create(alarm_data) # Assuming alarm is not directly user-specific, but tied to schedule
        return new_schedule

    def get_all_schedules(self, user_id):
        return self.repository.get_all(user_id)

    def get_schedule_by_id(self, user_id, id):
        return self.repository.get_by_id(user_id, id)

    def update_schedule(self, user_id, id, data):
        schedule = self.repository.get_by_id(user_id, id)
        if not schedule:
            return None
        updated_schedule = self.repository.update(user_id, schedule, data)
        # Update alarm entry
        alarm = self.alarm_repository.get_by_schedule_id(updated_schedule.id) # Assuming alarm is not directly user-specific, but tied to schedule
        if alarm:
            alarm_message = f"{updated_schedule.person}-{updated_schedule.description}"
            alarm_data = {
                'message': alarm_message,
                'alert_at': updated_schedule.date.isoformat()
            }
            self.alarm_repository.update(alarm, alarm_data)
        return updated_schedule

    def delete_schedule(self, user_id, id):
        schedule = self.repository.get_by_id(user_id, id)
        if not schedule:
            return False
        # Delete alarm entry first
        alarm = self.alarm_repository.get_by_schedule_id(id) # Assuming alarm is not directly user-specific, but tied to schedule
        if alarm:
            self.alarm_repository.delete(alarm)
        self.repository.delete(user_id, schedule)
        return True

    def get_schedules_by_user_id(self, user_id):
        return self.repository.get_schedules_by_user_id(user_id)