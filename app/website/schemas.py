from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.website.models import (
    Company,
    Service,
    SocialLink,
    Setting
)
from app.core.errors import ValidationError



class CompanySchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Company
        load_instance = True

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


class ServiceSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Service
        load_instance = True

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)


class SocialLinkSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = SocialLink
        load_instance = True

social_link_schema = SocialLinkSchema()
social_links_schema = SocialLinkSchema(many=True)



class SettingSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Setting
        load_instance = True

setting_schema = SettingSchema()
settings_schema = SettingSchema(many=True)



def validate_company_payload(data):

    if not data:
        raise ValidationError("No data provided")
    
    if not data.get("name"):
        raise ValidationError("Company name is required")
    
    return {
        "name" : data.get("name"),
        "phone" : data.get("phone"),
        "email" : data.get("email"),
        "about" : data.get("about"),
        "mission" : data.get("mission"),
        "vision" : data.get("vision"),
        "address" : data.get("address"),
        "logo" : data.get("logo")
    }

def validate_service_payload(data):
    if not data:
        raise ValidationError("No data provided.")
    
    if not data.get("name"):
        raise ValidationError("Service Name is required.")
    
    price = data.get('price')
    
    if price is not None and price < 0:
        raise ValidationError("Price cannot be negetive")
    
    return {
        "name" : data.get('name'), 
        "slug" : data.get('slug'), 
        "description" : data.get('description'), 
        "price" : data.get('price'), 
        "pricing_type" : data.get('pricing_type' , 'qoute'), 
        "is_active" : data.get(
            "is_active",
            True 
        )
    }

def validate_social_link(data):
    if not data:
        raise ValidationError('No data provided')
    
    if not data.get('platform'):
        raise ValidationError("Platform is required")
    
    if not data.get('url'):
        raise ValidationError("Url is required")
    
    return {
        "platform": data['platform'],
        "url" : data['url'],
        "icon" : data.get('icon'),
        "is_visible" : data.get(
            'is_visible',
            True
        )
    }

def validate_setting_payload(data):

    if not data:
        raise ValidationError(
            "No data provided."
        )
    if not data.get('key'):
        raise ValidationError(
            "Key is required."
        )
    
    return {
        "key" : data["key"],
        "value" : data.get("value"),
        "group" : data.get(
            "group",
            "general"
        )
    }



