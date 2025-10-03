import json
import logging
from kafka import KafkaProducer
from datetime import datetime, timedelta
import pytz

logger = logging.getLogger(__name__)

class KafkaScheduleProducer:
    def __init__(self, bootstrap_servers='192.168.219.107:9092'):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(0, 10, 1)
            )
            self.save_topic = 'save-schedule'
            self.delete_topic = 'delete-schedule'
            logger.info(f"Kafka producer initialized successfully with server: {bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            self.producer = None

    def send_schedule_alerts(self, schedule_id, description, person, date,
                            notify_one_hour_before=False, notify_one_day_before=False):
        """
        Send alert messages to Kafka based on notification settings.

        Args:
            schedule_id: Schedule ID
            description: Schedule description
            person: Person associated with schedule
            date: Schedule date (datetime object)
            notify_one_hour_before: Whether to send 1 hour before alert
            notify_one_day_before: Whether to send 1 day before alert
        """
        if not self.producer:
            logger.warning("Kafka producer not available. Skipping message publishing.")
            return

        kst = pytz.timezone('Asia/Seoul')

        # Convert date to KST if not already timezone-aware
        if date.tzinfo is None:
            date = kst.localize(date)
        else:
            date = date.astimezone(kst)

        base_message = {
            'message': description,
            'person': person,
            'schedule_id': schedule_id
        }

        messages = []

        # Alert at exact time
        messages.append({
            **base_message,
            'alert_at': date.isoformat()
        })

        # Alert 1 hour before
        if notify_one_hour_before:
            one_hour_before = date - timedelta(hours=1)
            messages.append({
                **base_message,
                'alert_at': one_hour_before.isoformat()
            })

        # Alert 1 day before
        if notify_one_day_before:
            one_day_before = date - timedelta(days=1)
            messages.append({
                **base_message,
                'alert_at': one_day_before.isoformat()
            })

        # Send all messages
        for message in messages:
            try:
                future = self.producer.send(self.save_topic, value=message)
                future.get(timeout=10)
                logger.info(f"Successfully sent message to Kafka: {message}")
            except Exception as e:
                logger.error(f"Failed to send message to Kafka: {e}. Message: {message}")

    def send_delete_schedule(self, schedule_id):
        """
        Send delete schedule message to Kafka.

        Args:
            schedule_id: Schedule ID to delete
        """
        if not self.producer:
            logger.warning("Kafka producer not available. Skipping message publishing.")
            return

        message = {
            'schedule_id': schedule_id
        }

        try:
            future = self.producer.send(self.delete_topic, value=message)
            future.get(timeout=10)
            logger.info(f"Successfully sent delete message to Kafka: {message}")
        except Exception as e:
            logger.error(f"Failed to send delete message to Kafka: {e}. Message: {message}")

    def close(self):
        """Close the Kafka producer connection."""
        if self.producer:
            try:
                self.producer.flush()
                self.producer.close()
                logger.info("Kafka producer closed successfully")
            except Exception as e:
                logger.error(f"Error closing Kafka producer: {e}")
