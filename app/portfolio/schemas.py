from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.core.errors import ValidationError
from app.core.slug import generate_slug
from app.portfolio.models import Category, Project, Image
from datetime import datetime


class CategorySchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Category
        load_instance = True


def validate_category_payload(data):

    if not data:
        raise ValidationError(
            "No data provided"
        )
    
    if not data.get('name'):
        raise ValidationError(
            "Category name is required."
        )
    
    return {
        "name" : data.get('name'),
        "slug" : generate_slug(data['name']),
        "description" : data.get('description'),
        "is_active" : data.get(
            "is_active", 
            True
        )
    }



class ProjectSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Project
        load_instance = True


def validate_project_payload(data):
    if not data:
        raise ValidationError(
            "No Data provided."
        )
    
    if not data.get("category_id"):
        raise ValidationError(
            "Category is required."
        )
    
    if not data.get('title'):
        raise ValidationError(
            "Project title is required."
        )

    
    if 'completed_at' in data and data['completed_at']:
        try:
            data['completed_at'] = datetime.strptime(
                data['completed_at'],
                "%Y-%m-%d"
            ).date()
        
        except (ValueError, TypeError):
            raise ValidationError(
                "completed_at must be in YYYY-MM-DD format"
            )
        
    elif "complited_at" in data:
        data['completed_at'] = None


    return {
        "category_id" : data["category_id"],
        "title" : data["title"],
        "client" : data.get("client"),
        "short_description" : data.get("short_description"),
        "description" : data.get("description"),
        "location":data.get("location"),
        "completed_at" : data.get("completed_at"),
        "is_featured" : data.get(
            "is_featured",
            False
        ),
        "is_active" : data.get("is_active", True)
    }


class ImageSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Image
        load_instance = True

def validate_image_payload(data):

    if data is None:
        raise ValidationError(
            "No data Provided"
        )
    
    return {
        "caption" : data.get("caption"),
        "display_order" : data.get(
            "display_order",
            0
        )
    }

    

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


image_schema = ImageSchema()
images_schema = ImageSchema(many=True)
