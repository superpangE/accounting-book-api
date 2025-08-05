from flask import Blueprint, request, jsonify
from services.accounting_book_service import AccountingBookService
from datetime import date

accounting_book_bp = Blueprint('accounting_book', __name__)
service = AccountingBookService()

@accounting_book_bp.route('/accounting-book', methods=['POST'])
def create_accounting_entry():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        new_entry = service.create_entry(data)
        return jsonify(new_entry.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {e}. Use YYYY-MM-DD"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@accounting_book_bp.route('/accounting-book/<int:id>', methods=['GET'])
def get_accounting_entry(id):
    entry = service.get_entry(id)
    if not entry:
        return jsonify({"error": "Entry not found"}), 404
    return jsonify(entry.to_dict())

@accounting_book_bp.route('/accounting-book/<int:id>', methods=['PATCH'])
def update_accounting_entry(id):
    data = request.get_json()
    if not data or 'is_send' not in data:
        return jsonify({"error": "Invalid JSON or missing 'is_send' field"}), 400

    try:
        # Only allow updating is_send field
        update_data = {'is_send': data['is_send']}
        updated_entry = service.update_entry(id, update_data)
        if not updated_entry:
            return jsonify({"error": "Entry not found"}), 404
        return jsonify(updated_entry.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@accounting_book_bp.route('/accounting-book/<int:id>', methods=['DELETE'])
def delete_accounting_entry(id):
    deleted = service.delete_entry(id)
    if not deleted:
        return jsonify({"error": "Entry not found"}), 404
    return '', 204

@accounting_book_bp.route('/accounting-book', methods=['GET'])
def list_accounting_entries():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        entries = service.list_entries(start_date, end_date)
        return jsonify([entry.to_dict() for entry in entries])
    except ValueError as e:
        return jsonify({"error": f"Invalid date format for start_date or end_date: {e}. Use YYYY-MM-DD"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
