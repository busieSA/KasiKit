from flask import Blueprint, request
from app.core.responses import success
from app.website.service import (
    CompanyService,
    ServiceService,
    SocialLinkService,
    SettingsService
)
from app.website.schemas import (
    validate_company_payload,
    validate_service_payload,
    validate_social_link,
    validate_setting_payload,
    company_schema,
    service_schema,
    services_schema,
    social_link_schema,
    social_links_schema, 
    setting_schema,
    settings_schema
)

website_bp = Blueprint("website", __name__, url_prefix='/')

###=============================== Services =================================###

company_service = CompanyService()
service_service = ServiceService()
social_service = SocialLinkService()
settings_service = SettingsService()
###============================= Routes ===================================###


@website_bp.post('/company')
def create_company():

    data = request.get_json()

    clean_data = validate_company_payload(data)

    company = company_service.create_company(clean_data)

    return success(
        company_schema.dump(company),
        "Company created successfully"
    )


@website_bp.get('/company')
def get_company():

    company = company_service.get_company()

    return success(
        company_schema.dump(company)
    )



@website_bp.put('/company')
def update_company():

    data = request.get_json()
    
    clean_data = validate_company_payload(data)
    
    company = company_service.update_company(clean_data)
    
    return success(
        company_schema.dump(company),
        "Company updated successfully"
    )




###=============================== Services =================================###

@website_bp.post('/services')
def create_service():

    data = request.get_json()

    clean = validate_service_payload(data)

    service = service_service.create_service(clean)

    return success(
        service_schema.dump(service),
        "Service created successfully"
    )



@website_bp.get('/services')
def get_services():

    services = service_service.get_all_services()

    return success(
        services_schema.dump(services)
    )



@website_bp.get('/services/<int: service_id>')
def get_service(service_id):

    service = service_service.get_service(service_id)
    
    return success(
        service_schema.dump(service)
    )



@website_bp.put('/services/<int:service_id>')
def update_service(service_id):

    data = request.get_json()

    clean = validate_service_payload(data)

    service = service_service.update_service(
        service_id,
        clean
    )

    return success(
        service_schema.dump(service)
    )




@website_bp.patch("/services/<int:service_id>/toggle")
def toggle_service(service_id):

    service = service_service.toggle_status(service_id)

    return success(
        service_schema.dump(service)
    )



@website_bp.delete('/services/<int:service_id>')
def delete_service(service_id):

    service_service.delete_service(service_id)

    return success(
        message='Service deleted successfully.'
    )


###=============================== Social Links =================================###

@website_bp.post("/social-links")
def create_social_link():

    data = request.get_json()
    
    clean = validate_social_link(data)
    
    link = social_service.create_link(clean)
    
    return success(
        social_link_schema.dump(link),
        "Social link created successfully."
    )



# Public End point
@website_bp.get('/social-links')
def get_social_links():

    links = social_service.get_visible()

    return success(
        social_links_schema.dump(links)
    )


###=============================== Settings =================================###

@website_bp.post('/settings')
def save_setting():

    data = request.get_json()

    clean = validate_setting_payload(data)

    setting = settings_service.save_setting(clean)

    return success(
        setting_schema.dump(setting)
    )

@website_bp.get('/settings/<string:key>')
def get_setting(key):

    setting = settings_service.get_setting(key)

    return success(
        setting_schema.dump(setting)
    )

@website_bp.get("/settings")
def get_settings():

    settings = settings_service.get_all_settings()

    return success(
        settings_schema.dump(settings)
    )




