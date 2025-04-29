from flask import Blueprint, request, jsonify
from your_model import read_where  # Haddii aad leedahay function la mid ah read_where

ajax_bp = Blueprint('ajax', __name__)

@ajax_bp.route('/ajax', methods=['POST'])
def handle_ajax():
    action = request.form.get('action')
    
    if action == 'forUpdate':
        table = request.form.get('table')
        id_value = request.form.get('id')
        
        # call the database function
        result = read_where(table, f"id = {id_value}")
        
        if result:
            return jsonify(result[0])
        else:
            return jsonify({'error': 'No record found'}), 404

    elif action == 'forPayment':
        member_id = request.form.get('memberid')
        
        # call the database function
        result = read_where("chargesveiw", f"member_id = {member_id} and status = 'Unpaid'")
        
        return jsonify(result)

    else:
        return jsonify({'error': 'Invalid action'}), 400
