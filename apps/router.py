from flask import Blueprint
from flask_restful import Api

from apps.controller.celery_task_controller import celery_task_bp
from apps.controller.celery_task_controller import CeleryResultResource
from apps.controller.celery_task_controller import CeleryResultListResource

from apps.controller.check_url_status_controller import check_url_status_bp
from apps.controller.check_url_status_controller import CheckURLStatusController
from apps.controller.check_url_status_controller import CheckUrlListController
from apps.controller.check_url_status_controller import CheckUrlController

from apps.controller.check_domain_certificate_controller import check_domain_certificate_bp
from apps.controller.check_domain_certificate_controller import CheckDomainCertificateController
from apps.controller.check_domain_certificate_controller import CheckDomainListController
from apps.controller.check_domain_certificate_controller import CheckDomainController

def register_router():
    celery_task_bp_api = Api(celery_task_bp)
    celery_task_bp_api.add_resource(CeleryResultResource, "/api/v1/tasks/<task_id>")
    celery_task_bp_api.add_resource(CeleryResultListResource, "/api/v1/tasks")
    
    check_url_status_bp_api = Api(check_url_status_bp)
    check_url_status_bp_api.add_resource(CheckUrlController, "/api/v1/check_url_create")
    check_url_status_bp_api.add_resource(CheckUrlListController, "/api/v1/check_url_list")
    check_url_status_bp_api.add_resource(CheckURLStatusController, "/api/v1/tasks/check_url_status")
    
    check_domain_certificate_bp_api = Api(check_domain_certificate_bp)
    check_domain_certificate_bp_api.add_resource(CheckDomainController, "/api/v1/check_domain_create")
    check_domain_certificate_bp_api.add_resource(CheckDomainListController, "/api/v1/check_domain_list")
    check_domain_certificate_bp_api.add_resource(CheckDomainCertificateController, "/api/v1/tasks/check_domain_certificate")
    
def register_blueprints(app):
    app.register_blueprint(celery_task_bp)
    app.register_blueprint(check_url_status_bp)
    app.register_blueprint(check_domain_certificate_bp)
    return app

