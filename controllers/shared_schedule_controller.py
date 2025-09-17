from flask import Blueprint, request, jsonify, g
from services.shared_schedule_service import SharedScheduleService
from datetime import datetime
from utils.auth_middleware import token_required

shared_schedule_bp = Blueprint('shared_schedule', __name__)
service = SharedScheduleService()

@shared_schedule_bp.route('/shared-schedules', methods=['POST'])
@token_required
def create_shared_schedule():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        new_schedule = service.create_schedule(g.user_id, data)
        return jsonify(new_schedule.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {e}. Use YYYY-MM-DDTHH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules', methods=['GET'])
@token_required
def get_all_shared_schedules():
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else None

        schedules = service.get_all_schedules(g.user_id, start_date, end_date)
        return jsonify([schedule.to_dict() for schedule in schedules]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules/<int:id>', methods=['GET'])
@token_required
def get_shared_schedule_by_id(id):
    try:
        schedule = service.get_schedule_by_id(g.user_id, id)
        if not schedule:
            return jsonify({"error": "Schedule not found"}), 404
        return jsonify(schedule.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules/<int:id>', methods=['PUT'])
@token_required
def update_shared_schedule(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        updated_schedule = service.update_schedule(g.user_id, id, data)
        if not updated_schedule:
            return jsonify({"error": "Schedule not found"}), 404
        return jsonify(updated_schedule.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {e}. Use YYYY-MM-DDTHH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules/<int:id>', methods=['DELETE'])
@token_required
def delete_shared_schedule(id):
    try:
        deleted = service.delete_schedule(g.user_id, id)
        if not deleted:
            return jsonify({"error": "Schedule not found"}), 404
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shared_schedule_bp.route('/shared-schedules/user', methods=['GET']) # Removed user_id from URL
@token_required
def get_shared_schedules_by_user_id():
    try:
        schedules = service.get_schedules_by_user_id(g.user_id)
        return jsonify([schedule.to_dict() for schedule in schedules]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500