from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from app.utils.validators import token_required

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    response, status_code = TaskService.create_task(current_user.id, request.get_json())
    return jsonify(response), status_code

@task_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    filters = request.args.to_dict()
    response, status_code = TaskService.get_user_tasks(current_user.id, filters)
    return jsonify(response), status_code

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    response, status_code = TaskService.get_task(task_id, current_user.id)
    return jsonify(response), status_code

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    response, status_code = TaskService.update_task(task_id, current_user.id, request.get_json())
    return jsonify(response), status_code

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    response, status_code = TaskService.delete_task(task_id, current_user.id)
    return jsonify(response), status_code 