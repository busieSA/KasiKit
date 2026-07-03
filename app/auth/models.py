from app.core.extensions import db
from app.core.base_model import BaseModel

class AdminUser(BaseModel):
    __tablename__ = 'admin_users'
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash= db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
