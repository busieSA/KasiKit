from app.portfolio.repository import (
    CategoryRepository,
    ProjectRepository,
    ImageRepository
)

from app.portfolio.models import Category, Image, Project
from app.core.errors import ConflictError, NotFoundError
from app.core.file_service import FileService
from app.core.slug import generate_slug


class CategoryService:

    def __init__(self):
        self.repo = CategoryRepository()

    def create_category(self, data):

        existing = self.repo.get_by_slug(
            data['slug']
        )

        if existing:
            raise ConflictError(
                "Category slug already exists."
            )
        
        category = Category(**data)

        self.repo.add(category)
        self.repo.commit()

        return category
    
    def get_all_categories(self):

        return self.repo.get_all()
    
    def get_category(self, category_id):

        category = self.repo.get_by_id(category_id)

        if not category:
            raise NotFoundError(
                "Category not found."
            )
        
        return category
    
    def update_category(self, category_id, data):

        category = self.get_category(category_id)

        for key, value in data.items():
            setattr(category, key, value)

        self.repo.commit()

        return category
    
    def toggle_status(self, category_id):
        category = self.get_category(
            category_id
        )

        category.is_active = (
            not category.is_active
        )

        self.repo.commit()

        return category
    
    def delete_category(self, category_id):

        category = self.get_category(category_id)

        self.repo.delete(category)
        self.repo.commit()

    
class ProjectService:

    def __init__(self):
        self.repo = ProjectRepository()
        self.category_repo = CategoryRepository()

    
    def create_project(self, data):

        category = self.category_repo.get_by_id(
            data['category_id']
        )

        if not category:
            raise NotFoundError(
                "Category not found."
            )

        data["slug"] = generate_slug(
            data['title']
        )

        #Business rule
        existing = self.repo.get_by_slug(
            data["slug"]
        )

        if existing:
            raise ConflictError(
                "Project slug already exists."
            )
        
        # Now create
        project = Project(**data)

        self.repo.add(project)
        self.repo.commit()

        return project
    
    def get_all_projects(self):

        return self.repo.get_all()
    

    def get_project(self, project_id):

        project = self.repo.get_by_id(project_id)

        if not project:
            raise NotFoundError(
                "Project not found."
            )
        
        return project
    
    
    def update_project(
            self,
            project_id,
            data
    ):
        
        project = self.repo.get_by_id(
            project_id
        )

        if "title" in data:
            data['slug'] = generate_slug(
                data['title']
            )

        for key, value in data.items():
            setattr(project, key, value)

        self.repo.commit()

        return project
    
    def toggle_status(self, project_id):

        project = self.repo.get_by_id(project_id)

        project.is_active = (
            not project.is_active
        )

        self.repo.commit()

        return project

    def toggle_featured(self, project_id):

        project = self.repo.get_by_id(project_id)

        project.is_featured = (
            not project.is_featured
        )

        self.repo.commit()

        return project

    def delete_project(self, project_id):

        project = self.repo.get_by_id(project_id)

        self.repo.delete(project)
        self.repo.commit()


class ImageService:

    def __init__(self):

        self.repo = ImageRepository()

        self.project_repo = ProjectRepository()

        self.file_service = FileService()

    def upload_image(
            self,
            project_id,
            upload_file,
            caption=None
    ):
        project = self.project_repo.get_by_id(project_id)

        if not project:
            raise NotFoundError("Project not found")
        
        paths = self.file_service.save_project_image(
            project.slug,
            upload_file
        )

        image = Image(
            project_id=project.id,
            file_path=paths["file_path"],
            thumbnail_path=paths["thumbnail_path"],
            caption=caption
        )

        self.repo.add(image)
        self.repo.commit()

        return image
    

    def get_project_images(self , project_id):
        
        project = self.project_repo.get_by_id(project_id)

        if not project:
            raise NotFoundError(
                "Project not found"
            )
        
        return self.repo.get_by_project(project_id)
    

    def get_image(self, image_id):

        image = self.repo.get_by_id(image_id)

        if not image:
            raise NotFoundError(
                "Image doesn't exists."
            )
        return image


    def update_caption(self,image_id, caption):
        
        image = self.get_image(image_id)

        image.caption = caption

        self.repo.commit()
        
        return image
    

    def update_display_order(self, image_id, display_order):
        
        image = self.get_image(image_id)

        image.display_order = display_order

        self.repo.commit()

        return image
    

    def replace_image(
            self,
            image_id,
            uploaded_file
    ):
        
        image = self.get_image(image_id)

        project = image.project

        self.file_service.delete_image(image.file_path)

        self.file_service.delete_image(image.thumbnail_path)

        paths = self.file_service.save_project_image(
            project.slug,
            uploaded_file
        )

    #Update database 

        image.file_path = paths["file_path"]
        image.thumbnail_path = paths["thumbnail_path"]

        self.repo.commit()

        return image
    
    
    def delete_image(self, image_id):

        image = self.get_image(image_id)

        project = image.project

    #Delete Original 
        self.file_service.delete_image(
            image.file_path
        )

    # delete Thumbnail
        self.file_service.delete_image(
            image.thumbnail_path
        )
    
    #Delete db record
        self.repo.delete(image)
        self.repo.commit()

    #remove empty project folder if last image.
        self.file_service.delete_project_folder_if_empty(
            project.slug
        )









