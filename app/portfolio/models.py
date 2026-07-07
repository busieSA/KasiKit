from app.core.extensions import db
from app.core.base_model import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'
    name = db.Column(db.String(120), nullable=False, unique=True)
    slug = db.Column(db.String(140), unique=True, index=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


    projects = db.relationship('Project', back_populates='category', cascade='all, delete-orphan', lazy=True)


class Project(BaseModel):

    __tablename__ = 'projects'

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, index=True)
    client = db.Column(db.String(200))

    short_description = db.Column(db.Text)
    description = db.Column(db.Text)
    location = db.Column(db.String(150))

    completed_at = db.Column(db.Date) 

    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    

    images = db.relationship('Image', backref='project',lazy=True, cascade='all, delete-orphan')
    category = db.relationship('Category', back_populates='projects')

class Image(BaseModel):
    __tablename__  = 'images'

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False )
    
    file_path = db.Column(db.String(255), nullable=False)
    thumbnail_path = db.Column(db.String(255))
    caption = db.Column(db.String(255))

    display_order = db.Column(db.Integer,default=0)


