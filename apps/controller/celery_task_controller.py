from flask import Blueprint, current_app
from flask_restful import Resource
from apps.extensions import db
from apps.models import CeleryTaskMetaModel
from sqlalchemy import Select
from celery.result import AsyncResult

celery_task_bp = Blueprint("celery_task", __name__)

class CeleryResultResource(Resource):
    def get(self, task_id):
        query = Select(CeleryTaskMetaModel).filter_by(task_id=task_id)
        task = db.session.scalars(query).first()
        if not task:
            return {"error": "Task not found"}
        result = AsyncResult(task_id)
        ready = result.ready()
        if ready:
            return {
                "task_id": result.task_id,
                "date_done": result.date_done.strftime("%Y-%m-%d %H:%M:%S%z"),
                "ready": ready,
                "successful": result.successful() if ready else None,
                "data": result.get() if ready else result.result
            }
    
class CeleryResultListResource(Resource):
    def post(self):
        task_list = db.session.scalars(Select(CeleryTaskMetaModel)).all()
        return [task.to_dict() for task in task_list]