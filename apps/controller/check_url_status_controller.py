from flask import Blueprint, current_app, request
from flask_restful import Resource
from apps.extensions import db
from apps.models import UrlModel
from sqlalchemy import Select
from apps.celery_tasks.check_url_status import check_url_status
from validators import url as is_url

check_url_status_bp = Blueprint("check_url_status", __name__)

def check_is_url(url):
    if is_url(url):
        return True

def get_url_list():
    query = Select(UrlModel)
    return db.session.scalars(query).all()

class CheckURLStatusController(Resource):
    def post(self):
        url_list = get_url_list()
        result = [check_url_status.delay(ck.url) for ck in url_list if ck.status]
        return [{"task_id": task.id} for task in result]

class CheckUrlListController(Resource):
    def post(self):
        url_list = get_url_list()
        return [url.to_dict() for url in url_list]
    
class CheckUrlController(Resource):
    def post(self):
        url = request.json.get("url", None)
        if not check_is_url(url):
            return {
                "url": url,
                "error": "URL不正确"
            }
        query = Select(UrlModel).filter_by(url=url)
        result = db.session.scalars(query).first()
        if result:
            return {"error": f"{url} 已存在"}
        new_url = UrlModel(url=url)
        db.session.add(new_url)
        db.session.commit()
        return {"msg": f"{url} 创建成功"}
    
    def put(self):
        pass 
    
    def delete(self):
        pass 
