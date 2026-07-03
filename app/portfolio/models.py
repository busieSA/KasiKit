from app.core.extensions import db
from app.core.base_model import BaseModel

class PortfolioCategory(BaseModel):
    __tablename__ = 'portfolio_categories'
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, index=True)
    description = db.Column(db.Text)

    projects = db.relationship('Project', backref='category', lazy=True)


class Project(BaseModel):
    __tablename__ = 'projects'
    category_id = db.Column(db.Integer, db.FoerignKey('portfolio_categories.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, index=True)

    description = db.Column(db.Text)
    location = db.Column(db.String(150))

    start_date = db.Column(db.Date) 
    end_date   = db.Column(db.Date)

    is_featured = db.Column(db.Boolean, default=False)

    images = db.relationship('Image', backref='project',lazy=True, cascade='all, delete-orphan')

class Image(BaseModel):
    __tablename__  = 'images'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False )
    file_path = db.Column(db.String(255), nullable=False)
    thumbnail_path = db.Column(db.String(255))
    caption = db.Column(db.String(255))

    display_order = db.Column(db.Integer,defaul=0)


