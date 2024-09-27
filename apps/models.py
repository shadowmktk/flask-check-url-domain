from apps.extensions import db

class UrlModel(db.Model):
    __tablename__ = "task_url"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    url: db.Mapped[str] = db.mapped_column(db.String(155))
    status: db.Mapped[bool] = db.mapped_column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"<UrlModel {self.id},{self.url}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "status": self.status
        }
    
class DomainModel(db.Model):
    __tablename__ = "task_domain"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    domain: db.Mapped[str] = db.mapped_column(db.String(155))
    port: db.Mapped[int] = db.mapped_column(db.Integer)
    status: db.Mapped[bool] = db.mapped_column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"<DomainModel {self.id},{self.domain}>"

    def to_dict(self):
        return {
            "id": self.id,
            "domain": self.domain,
            "port": self.port,
            "status": self.status
        }
        
class CeleryTaskMetaModel(db.Model):
    __tablename__ = "celery_taskmeta"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    task_id: db.Mapped[str] = db.mapped_column(db.String(155), unique=True)
    status: db.Mapped[str] = db.mapped_column(db.String(50), nullable=True)
    result: db.Mapped[str] = db.mapped_column(db.LargeBinary, nullable=True)
    date_done: db.Mapped[db.DateTime] = db.mapped_column(db.DateTime, nullable=True)
    traceback: db.Mapped[str] = db.mapped_column(db.Text(155), nullable=True)
    name: db.Mapped[str] = db.mapped_column(db.String(155), nullable=True)
    args: db.Mapped[str] = db.mapped_column(db.LargeBinary, nullable=True)
    kwargs: db.Mapped[str] = db.mapped_column(db.LargeBinary, nullable=True)
    worker: db.Mapped[str] = db.mapped_column(db.String(155), nullable=True)
    retries: db.Mapped[int] = db.mapped_column(db.Integer, nullable=True)
    queue: db.Mapped[str] = db.mapped_column(db.String(155), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "status": self.status,
            "date_done": self.date_done.strftime("%Y-%m-%d %H:%M:%S%z")
        }
        