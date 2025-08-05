from flask import Blueprint, request, jsonify
from services.shared_schedule_service import SharedScheduleService
from datetime import datetime

shared_schedule_bp = Blueprint('shared_schedule', __name__)
service = SharedScheduleService()

@shared_schedule_bp.route('/shared-schedules', methods=['POST'])
def create_shared_schedule():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        new_schedule = service.create_schedule(data)
        return jsonify(new_schedule.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {e}. Use YYYY-MM-DDTHH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules', methods=['GET'])
def get_all_shared_schedules():
    try:
        schedules = service.get_all_schedules()
        return jsonify([schedule.to_dict() for schedule in schedules]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules/<int:id>', methods=['GET'])
def get_shared_schedule_by_id(id):
    try:
        schedule = service.get_schedule_by_id(id)
        if not schedule:
            return jsonify({"error": "Schedule not found"}), 404
        return jsonify(schedule.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules/<int:id>', methods=['PUT'])
def update_shared_schedule(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        updated_schedule = service.update_schedule(id, data)
        if not updated_schedule:
            return jsonify({"error": "Schedule not found"}), 404
        return jsonify(updated_schedule.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {e}. Use YYYY-MM-DDTHH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules/<int:id>', methods=['DELETE'])
def delete_shared_schedule(id):
    try:
        deleted = service.delete_schedule(id)
        if not deleted:
            return jsonify({"error": "Schedule not found"}), 404
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500