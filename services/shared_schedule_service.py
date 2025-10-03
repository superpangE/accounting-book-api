from repositories.shared_schedule_repository import SharedScheduleRepository
from utils.kafka_producer import KafkaScheduleProducer
import logging

logger = logging.getLogger(__name__)

class SharedScheduleService:
    def __init__(self):
        self.repository = SharedScheduleRepository()
        self.kafka_producer = KafkaScheduleProducer()

    def create_schedule(self, user_id, data):
        new_schedule = self.repository.create(user_id, data)

        # Send Kafka messages (failures won't affect API response)
        try:
            self.kafka_producer.send_schedule_alerts(
                schedule_id=new_schedule.id,
                description=new_schedule.description,
                person=new_schedule.person,
                date=new_schedule.date,
                notify_one_hour_before=new_schedule.notify_one_hour_before,
                notify_one_day_before=new_schedule.notify_one_day_before
            )
        except Exception as e:
            logger.error(f"Failed to send Kafka message for schedule {new_schedule.id}: {e}")

        return new_schedule

    def get_all_schedules(self, user_id, start_date=None, end_date=None):
        return self.repository.get_all(user_id, start_date, end_date)

    def get_schedule_by_id(self, user_id, id):
        return self.repository.get_by_id(user_id, id)

    def update_schedule(self, user_id, id, data):
        schedule = self.repository.get_by_id(user_id, id)
        if not schedule:
            return None
        updated_schedule = self.repository.update(user_id, schedule, data)

        # Send Kafka messages (failures won't affect API response)
        try:
            # First, delete old schedule alerts
            self.kafka_producer.send_delete_schedule(schedule_id=updated_schedule.id)

            # Then, send new schedule alerts with updated information
            self.kafka_producer.send_schedule_alerts(
                schedule_id=updated_schedule.id,
                description=updated_schedule.description,
                person=updated_schedule.person,
                date=updated_schedule.date,
                notify_one_hour_before=updated_schedule.notify_one_hour_before,
                notify_one_day_before=updated_schedule.notify_one_day_before
            )
        except Exception as e:
            logger.error(f"Failed to send Kafka message for updated schedule {updated_schedule.id}: {e}")

        return updated_schedule

    def delete_schedule(self, user_id, id):
        schedule = self.repository.get_by_id(user_id, id)
        if not schedule:
            return False

        # Send Kafka delete message (failures won't affect API response)
        try:
            self.kafka_producer.send_delete_schedule(schedule_id=id)
        except Exception as e:
            logger.error(f"Failed to send Kafka delete message for schedule {id}: {e}")

        self.repository.delete(user_id, schedule)
        return True

    def get_schedules_by_user_id(self, user_id):
        return self.repository.get_schedules_by_user_id(user_id)