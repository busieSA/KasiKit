from app.auth.models import AdminUser
from app.core.base_repository import BaseRepository


class AdminRepository(BaseRepository):
    def __init__(self):
        super().__init__(AdminUser)
    
    def get_by_username(self, username):
        return self.model.query.filter_by(username=username).first()

    def activate(self, user):
        user.is_active = True
        self.commit()

    def deactivate(self, user):
        user.is_active = False
        self.commit()

    