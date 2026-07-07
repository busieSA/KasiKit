from app.core.base_repository import BaseRepository
from app.website.models import Company, Service, SocialLink, Setting



class CompanyRepository(BaseRepository):

    def __init__(self):
        super().__init__(Company)
    
    ## Domain Specific
    def get_company(self):
        """ system has only one company """
        return self.model.query.first()
    
    def company_exists(self):
        return self.model.query.first() is not None
    



class ServiceRepository(BaseRepository):

    def __init__(self):
        super().__init__(Service)
    
    def get_by_company(self, company_id):
        return self.model.query.filer_by(company_id=company_id).all()
    
    def get_active_services(self):
        return self.model.query.filter_by(is_active=True).all()
    
    def get_by_slug(self, slug):
        return self.model.query.filter_by(slug=slug).first()




class SocialLinkRepository(BaseRepository):

    def __init__(self):
        super().__init__(SocialLink)
    
    def get_visible(self):
        return self.model.query.filter_by(is_visible=True).all()
    
    def get_visible(self):
        return (
            self.model.query
            .filter_by(
                is_visible=True
            ).all()
        )
    
    def get_by_platform(self,platform):
        return (
            self.model.query
            .filter_by(platform=platform).first()
        )


class SettingsRepository(BaseRepository):

    def __init__(self):
        super().__init__(Setting)
    
    def get_by_key(self, key):
        return (
            self.model.query.filter_by(
                key=key
            ).first()
        )
    
    def get_all_settings(self):
        
        return self.get_all()


    def get_value(self, key, default=None):
        setting = self.model.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    def set_value(self, key, value, group=None):
        setting = self.model.query.filter_by(key=key).first()

        if setting:
            setting.value=value
        else:
            setting = Setting(key=key, value=value, group=group)
            self.add(setting)
        self.commit()
        return setting
    
    


