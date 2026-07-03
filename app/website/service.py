from app.website.repository import (
    CompanyRepository,
    ServiceRepository,
    SocialLinkRepository,
    SettingsRepository
)

from app.website.models import Company, Service, SocialLink, Setting

from app.core.errors import ConflictError, NotFoundError



class CompanyService:

    def __init__(self):
        self.repo = CompanyRepository()

    ## Create Company (BUSINESS RULE : SINGLETON)
    def create_company(self, data):
        if self.repo.company_exists():
            raise ConflictError("Company already exists")
        
        company = Company(**data)
        self.repo.add(company)
        self.repo.commit()

        return company
    
    ## Get COMPANY
    def get_company(self):
        company = self.repo.get_company()

        if not company:
            raise NotFoundError("Company not found.")
        
        return company
    
    ## Update Company
    def update_company(self, data):
        company = self.repo.get_company()
        if not company:
            raise NotFoundError("Company not found.")
        for key, value in data.items():
            setattr(company, key, value)
        self.repo.commit()
        return company
    

class ServiceService:
    def __init(self):
        self.repo = ServiceRepository()
    
    def create_service(self, data):
        if self.repo.get_by_slug(data.get("slug")):
            raise ConflictError("Service slug already exists")
        service = Service(**data)
        self.repo.add(service)
        self.repo.commit()
        return service
    
    def get_all_services(self):
        return self.repo.get_all()
    
    def get_service(self, service_id):
        service = self.repo.get_by_id(service_id)
        if not service:
            raise NotFoundError("Service not found")

        return service
    
    def update_service(self, service_id, data):
        service = self.repo.get_by_id(service_id)
        if not service:
            raise NotFoundError("Service not found")

        for key, value in data.items():
            setattr(service, key, value)

        self.repo.commit()
        return service
    

    def toggle_status(self, service_id):
        service = self.repo.get_by_id(service_id)
        if not service:
            raise NotFoundError("Service not found")
        
        service.is_active = not service.is_active
        self.repo.commit()
        return service
    
    def delete_service(self, service_id):
        service = self.repo.get_by_id(service_id)

        if not service:
            raise NotFoundError("Service not found")
        
        self.repo.add(service)
        self.repo.commit()

class SocialLinkService:
    def __init__(self):
        self.repo = SocialLinkRepository()

    def get_visible(self):
        return (
            self.repo.get_visible()
        )
    
    def create_link(self,data):
        if self.repo.get_by_platform(
            data['platform']
        ): 
            raise ConflictError("Platform already exists")
        link = SocialLink(**data)
        self.repo.add(link)
        self.repo.commit()

        return link 

    def update_link(self, link_id, data):
        link = self.repo.get_by_id(link_id)
        if not link:
            raise NotFoundError("Social link not found")
        
        for key, value in data.items():
            setattr(link, key, value)
        
        self.repo.commit()
        return link
    
    def toggle_visibility(self, link_id):
        link = self.repo.get_by_id(link_id)

        if not link:
            raise NotFoundError("Social link not found")
        
        link.is_visible = not link.is_visible

        self.repo.commit()
        
        return link
    
        
class SettingsService:

    def __init__(self):
        self.repo = SettingsRepository()

    def get_setting(self, key):
        
        setting = self.repo.get_by_key(key)

        if not setting:
            raise NotFoundError(
                "Setting not found."
            )
    ## Upsert pattern
    def save_setting(self, data):

        setting = self.repo.get_by_key(
            data['key']
        )

        ## if settings already exists update it 

        if setting:
            
            setting.value = data['value']

            setting.group = data.get('group')

            self.repo.commit()

            return setting
        
        ### Else create it
        else:
            setting = Setting(**data)

            self.repo.add(setting)

            self.repo.commit()

            return setting

    def get_all_settings(self):
        return  self.repo.get_all()


    
    