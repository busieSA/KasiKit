from flask import Blueprint, request
from app.core.responses import success
from app.core.error_handlers import ValidationError
from app.core.file_service import FileService
from app.portfolio.service import (
    CategoryService,
    ProjectService,
    ImageService
)

from app.portfolio.schemas import (
    validate_category_payload,
    category_schema,
    categories_schema,
    validate_project_payload,
    project_schema,
    projects_schema,
    validate_image_payload,
    image_schema,
    images_schema
)

portfolio_bp = Blueprint("portfolio", __name__, url_prefix='/api')

# services 
category_service = CategoryService()
project_service = ProjectService()
image_service = ImageService()

###=============================== Categories =================================###

@portfolio_bp.post('/categories')
def create_category():

    clean = validate_category_payload(
        request.get_json()
    )

    category = category_service.create_category(data=clean)

    return success(
        category_schema.dump(category),
        "Catgory created successfully."
    )

@portfolio_bp.get('/categories')
def get_catgories():

    categories = category_service.get_all_categories()

    return success(
        categories_schema.dump(categories)
    )

@portfolio_bp.get("/categories/<int:category_id>")
def get_category(category_id):

    category = category_service.get_category(category_id)

    return success(
        category_schema.dump(category)
    )

@portfolio_bp.put("/categories/<int:category_id>")
def update_category(category_id):

    data = validate_category_payload(
        request.get_json()
    )

    category = category_service.update_category(category_id,data)

    return success(
        category_schema.dump(category),
        "Category updated successfully."
    )

@portfolio_bp.patch("/categories/<int:category_id>/toggle")
def toggle_category(category_id):
    
    category = category_service.toggle_status(
        category_id
    ) 

    return success(
        category_schema.dump(category),
        "Category status updated."
    )

@portfolio_bp.delete("/categories/<int:category_id>")
def delete_category(category_id):

    category_service.delete_category(category_id)

    return success(
        message="Category deleted successfully."
    )

###=============================== Projects =================================###

@portfolio_bp.post('/projects')
def create_project():

    data = validate_project_payload(
        request.get_json()
    )

    project = project_service.create_project(data)

    return success(
        project_schema.dump(project),
        "Project created successfully."
    ), 201


@portfolio_bp.get('/projects')
def get_projects():

    projects = project_service.get_all_projects()

    return success(
        projects_schema.dump(projects)
    )

@portfolio_bp.get('/projects/<int:project_id>')
def get_project(project_id):

    project = project_service.get_project(project_id)

    return success(
        project_schema.dump(project)
    )

@portfolio_bp.put('/projects/<int:project_id>')
def update_project(project_id):

    data = validate_project_payload(
        request.get_json()
    )

    project = project_service.update_project(
        project_id,
        data
    )

    return success(
        project_schema.dump(project),
        "Project updated successfully."
    )

@portfolio_bp.patch('/projects/<int:project_id>/toggle')
def toggle_status(project_id):

    project = project_service.toggle_status(project_id)

    return success(
        project_schema.dump(project),
        "Project status updated"
    )

@portfolio_bp.patch('/projects/<int:project_id>/featured')
def toggle_featured(project_id):

    project = project_service.toggle_featured(project_id)

    return success(
        project_schema.dump(project),
        "Project featured status updated."
    )

@portfolio_bp.delete('/projects/<int:project_id>')
def delete_project(project_id):

    project_service.delete_project(project_id)

    return success(
        message="Project deleted successfully."
    )



###=============================== Images =================================###


@portfolio_bp.post('/projects/<int:project_id>/images')
def upload_image(project_id):

    image = request.files.get("image")

    if not image:
        raise ValidationError(
            "Image file is requeired."
        )
    
    caption = request.form.get("caption")

    uploaded = image_service.upload_image(
        project_id,
        image,
        caption
    ) 

    return success(
        message = "Image uploaded successfully.",
        data = image_schema.dump(uploaded)
    ), 201

@portfolio_bp.get('/projects/<int:project_id>/images')
def get_project_images(project_id):

    images = image_service.get_project_images(project_id)

    return success(
        data = images_schema.dump(images)
    )


@portfolio_bp.patch('/images/<int:image_id>/caption')
def update_caption(image_id):

    data = request.get_json()

    caption = data.get('caption')

    image = image_service.update_caption(
        image_id,
        caption
    )

    return success(
        message='Caption updated successfully.',
        data= image_schema.dump(image)
    )

@portfolio_bp.patch('/images/<int:image_id>/display-order')
def update_display_order(image_id):

    data = request.get_json()

    order = data.get(
        "display_order",
        0
    )

    image = image_service.update_display_order(
        image_id,
        order
    )

    return success(
        message= "Display order updated successfully.",
        data = image_schema.dump(image)
    )


@portfolio_bp.delete("/images/<int:image_id>/images")
def delete_image(image_id):
    
    image_service.delete_image(image_id)

    return success(
        message = "Image deleted successfully."
    )

@portfolio_bp.put("/images/<int:image_id>")
def replace_image(image_id):

    uploaded_file = request.files.get("image")

    if not uploaded_file:
        raise ValidationError(
            "Image File is required."
        )
    
    image = image_service.replace_image(image_id, uploaded_file)

    return success(
        data=image_schema.dump(image),
        message="Image replaced successfully."
    )

