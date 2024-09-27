from flask import Blueprint, current_app, request
from flask_restful import Resource
from apps.extensions import db
from apps.models import DomainModel
from sqlalchemy import Select
from apps.celery_tasks.check_domain_certificate import check_domain_certificate

from validators import domain as is_domain
from validators import ip_address

check_domain_certificate_bp = Blueprint("check_domain_certificate", __name__)

def check_is_domain(domain):
    if is_domain(domain):
        return True

def check_is_ip_address(ip):
    if ip_address.ipv4(ip):
        return True

def get_domain_list():
    query = Select(DomainModel)
    return db.session.scalars(query).all()

class CheckDomainCertificateController(Resource):
    def post(self):
        domain_list = get_domain_list()
        result = [check_domain_certificate.delay(dm.domain, dm.port) for dm in domain_list if dm.status]
        return  [{"task_id": task.id} for task in result]
    
class CheckDomainListController(Resource):
    def post(self):
        domain_list = get_domain_list()
        return [domain.to_dict() for domain in domain_list]

class CheckDomainController(Resource):
    def post(self):
        domain = request.json.get("domain", None)
        port = request.json.get("port", None)
        if not check_is_ip_address(domain) and not check_is_domain(domain):
            return {
                "domain": domain,
                "error": "域名不正确"
            }
        
        query = Select(DomainModel).filter_by(domain=domain)
        result = db.session.scalars(query).first()
        if result:
            return {"error": f"{domain} 已存在"}
        new_domain = DomainModel(domain=domain, port=port)
        db.session.add(new_domain)
        db.session.commit()
        return {"msg": f"{domain} 创建成功"}
    
    def put(self):
        pass 
    
    def delete(self):
        pass 
        
    
