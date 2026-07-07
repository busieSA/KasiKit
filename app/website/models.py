from app.core.extensions import db
from app.core.base_model import BaseModel

class Company(BaseModel):
    __tablename__ = 'company'
    name  = db.Column(db.String(150), nullable=False) 
    phone = db.Column(db.String(30))
    email = db.Column(db.String(150),unique=True)
    about = db.Column(db.Text)
    mission = db.Column(db.Text)
    vision = db.Column(db.Text)
    address = db.Column(db.Text)
    logo = db.Column(db.String(255))

    services = db.relationship('Service', backref='company', lazy=True)
    

class Service(BaseModel):
    __tablename__ = 'services'
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(160), unique=True,index=True)

    description = db.Column(db.Text)
    price = db.Column(db.Float)

    pricing_type = db.Column(db.String(20), default='quote')

class SocialLink(BaseModel):
    __tablename__ = 'social_links'
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    platform = db.Column(db.String(50), nullable=False)
    url= db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50))
    is_visible = db.Column(db.Boolean, default=True)

class Setting(BaseModel):
    __tablename__ = 'settings'
    key =  db.Column(db.String(100),unique=True, index=True)
    value = db.Column(db.Text)
    group = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=True)


