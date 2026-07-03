from app.portfolio.models import PortfolioCategory, Project, Image
from app.core.base_repository import BaseRepository

class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(PortfolioCategory)
    
    def get_by_slug(self, slug):
        return self.model.query.filter_by(slug=slug).first()
    
class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)
    
    def get_by_category(self, category_id):
        return self.model.query.filter_by(category_id=category_id).all()

    def get_by_featured(self):
        return self.model.query.filter_by(is_featured=True).all()
    
    def get_by_slug(self,slug):
        return self.model.query.filter_by(slug=slug).first()
    

class ImageRepository(BaseRepository):
    def __init__(self):
        super().__init__(Image)
    
    def get_by_project(self, project_id):
        return self.model.query.filter_by(project_id=project_id).order_by(Image.display_order).all()
    
    
