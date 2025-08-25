from flask import Blueprint, request, jsonify, g
from services.accounting_book_service import AccountingBookService
from datetime import date
from utils.auth_middleware import token_required

accounting_book_bp = Blueprint('accounting_book', __name__)
service = AccountingBookService()

@accounting_book_bp.route('/accounting-book', methods=['POST'])
@token_required
def create_accounting_entry():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        new_entry = service.create_entry(g.user_id, data)
        return jsonify(new_entry.to_dict()), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {e}. Use YYYY-MM-DD"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@accounting_book_bp.route('/accounting-book/<int:id>', methods=['GET'])
@token_required
def get_accounting_entry(id):
    entry = service.get_entry(g.user_id, id)
    if not entry:
        return jsonify({"error": "Entry not found"}), 404
    return jsonify(entry.to_dict())

@accounting_book_bp.route('/accounting-book/<int:id>', methods=['PATCH'])
@token_required
def update_accounting_entry(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    update_data = {}
    if 'is_send' in data:
        update_data['is_send'] = data['is_send']
    elif 'person' in data and 'category' in data:
        update_data['person'] = data['person']
        update_data['category'] = data['category']
    else:
        return jsonify({"error": "Invalid request body. Provide 'is_send' or both 'person' and 'category'"}), 400

    try:
        updated_entry = service.update_entry(g.user_id, id, update_data)
        if not updated_entry:
            return jsonify({"error": "Entry not found"}), 404
        return jsonify(updated_entry.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@accounting_book_bp.route('/accounting-book/<int:id>', methods=['DELETE'])
@token_required
def delete_accounting_entry(id):
    deleted = service.delete_entry(g.user_id, id)
    if not deleted:
        return jsonify({"error": "Entry not found"}), 404
    return '', 204

@accounting_book_bp.route('/accounting-book', methods=['GET'])
@token_required
def list_accounting_entries():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        entries = service.list_entries(g.user_id, start_date, end_date)
        return jsonify([entry.to_dict() for entry in entries])
    except ValueError as e:
        return jsonify({"error": f"Invalid date format for start_date or end_date: {e}. Use YYYY-MM-DD"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
