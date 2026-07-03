from app.core.extensions import db
from app.core.base_model import BaseModel


class Message(BaseModel):
    __tablename__ = 'messages'

    name = db.Column(db.String(120), nullable=False)
    email= db.Column(db.String(150), nullable=False)
    phone= db.Column(db.String(30))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    
    