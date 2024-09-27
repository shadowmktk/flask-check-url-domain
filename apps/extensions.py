from flask_sqlalchemy import SQLAlchemy
from celery import Celery, Task

db = SQLAlchemy()

def register_sqlalchemy(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

def register_celery(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery_app = Celery("celery", task_cls=FlaskTask)
    CELERY = dict(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery_app.config_from_object(CELERY)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
