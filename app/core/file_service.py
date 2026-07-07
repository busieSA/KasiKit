from pathlib import Path
from shutil import rmtree
from uuid import uuid4

from flask import current_app
from PIL import Image


class FileService:
    
    def __init__(self):
        # Absolute upload directory.
    
        self.upload_root = (
            Path(current_app.root_path)
            / current_app.config["UPLOAD_FOLDER"]
        )

    # --------------------------------------------------
    # PROJECT FOLDERS
    # --------------------------------------------------

    def create_project_folder(self, slug):

        folder = (
            self.upload_root
            / "projects"
            / slug
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return folder

    def get_project_folder(self, slug):

        return (
            self.upload_root
            / "projects"
            / slug
        )

    def project_folder_exists(self, slug):

        return self.get_project_folder(slug).exists()

    def delete_project_folder(self, slug):

        folder = self.get_project_folder(slug)

        if folder.exists():
            rmtree(folder)

    def rename_project_folder(
        self,
        old_slug,
        new_slug
    ):
        """
        Rename a project's folder.
        """

        old_folder = self.get_project_folder(old_slug)

        if not old_folder.exists():
            return

        new_folder = self.get_project_folder(new_slug)

        old_folder.rename(new_folder)

    def delete_project_folder_if_empty(self, slug):
        
        
        thumb_folder =(
            self.get_project_folder(slug)
            / "thumbnail"
        )

        if (
            thumb_folder.exists() and not any(thumb_folder.iterdir())
        ):
            thumb_folder.rmdir()
        
        folder = self.get_project_folder(slug)

        if (
            folder.exists() and not any(
                folder.iterdir()
            )
        ):
            folder.rmdir()





    # --------------------------------------------------
    # IMAGES
    # --------------------------------------------------

    def save_project_image(
        self,
        slug,
        uploaded_file
    ):
        
        # Create project folder
        folder = self.create_project_folder(slug)

        # Unique filename
        filename = f"{uuid4().hex}.webp"

        thumb_filename = filename

        # Absolute file path
        filepath = folder / filename

        thumb_folder = folder / "thumbnails"

        thumb_folder.mkdir(
            exist_ok=True
        )
        
        thumbnail_path = thumb_folder / thumb_filename

        # Open uploaded image
        image = Image.open(uploaded_file)

        # Convert to RGB
        image = image.convert("RGB")

        # Save Original as WebP
        image.save(
            filepath,          # <--Super IMPORTANT
            "WEBP",
            quality=85
        )

        #create thumbnail

        thumbnail = image.copy()
        thumbnail.thumbnail(
            (450,450)
        )

        thumbnail.save(
            thumbnail_path,
            "WEBP",
            quality=80
        )

        # Return relative path for database
        relative_path = (
            Path("projects")
            / slug
            / filename
        )

        return {
            "file_path": str(
                Path("projects")
                / slug 
                / filename
            ),
            
            "thumbnail_path" : str(
                Path("projects")
                / slug
                / "thumbnails"
                / thumb_filename
            )
        }


    def get_absolute_path(self, relative_path):
        
        return self.upload_root / relative_path
    
    def delete_image(self, relative_path):
        
        filepath = self.get_absolute_path(relative_path)

        if filepath.exists():
            filepath.unlink()

        