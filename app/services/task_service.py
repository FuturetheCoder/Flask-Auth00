from app import db
from app.models.task import Task
from datetime import datetime

class TaskService:
    @staticmethod
    def create_task(user_id, data):
        try:
            if not data.get('title'):
                return {'message': 'Title is required'}, 400

            due_date = None
            if data.get('due_date'):
                try:
                    due_date = datetime.fromisoformat(data['due_date'])
                except ValueError:
                    return {'message': 'Invalid date format. Use ISO format (YYYY-MM-DD)'}, 400

            task = Task(
                title=data['title'],
                description=data.get('description', ''),
                due_date=due_date,
                status=data.get('status', 'pending'),
                priority=data.get('priority', 'medium'),
                user_id=user_id
            )
            
            db.session.add(task)
            db.session.commit()
            return {'message': 'Task created successfully', 'task': task.to_dict}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to create task', 'error': str(e)}, 500

    @staticmethod
    def get_user_tasks(user_id, filters=None):
        try:
            query = Task.query.filter_by(user_id=user_id)
            
            if filters:
                if filters.get('status'):
                    query = query.filter_by(status=filters['status'])
                if filters.get('priority'):
                    query = query.filter_by(priority=filters['priority'])
            
            tasks = query.order_by(Task.created_at.desc()).all()
            return {'tasks': [task.to_dict for task in tasks]}, 200
        except Exception as e:
            return {'message': 'Failed to fetch tasks', 'error': str(e)}, 500

    @staticmethod
    def get_task(task_id, user_id):
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()
            if not task:
                return {'message': 'Task not found'}, 404
            return {'task': task.to_dict}, 200
        except Exception as e:
            return {'message': 'Failed to fetch task', 'error': str(e)}, 500

    @staticmethod
    def update_task(task_id, user_id, data):
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()
            if not task:
                return {'message': 'Task not found'}, 404

            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'status' in data:
                task.status = data['status']
            if 'priority' in data:
                task.priority = data['priority']
            if 'due_date' in data:
                try:
                    task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
                except ValueError:
                    return {'message': 'Invalid date format. Use ISO format (YYYY-MM-DD)'}, 400

            db.session.commit()
            return {'message': 'Task updated successfully', 'task': task.to_dict}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to update task', 'error': str(e)}, 500

    @staticmethod
    def delete_task(task_id, user_id):
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()
            if not task:
                return {'message': 'Task not found'}, 404

            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to delete task', 'error': str(e)}, 500 