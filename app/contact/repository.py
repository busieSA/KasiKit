from app.contact.models import Message
from app.core.base_repository import BaseRepository

class MessageRepository(BaseRepository):
    def __init__(self):
        super().__init__(Message)
    
    def get_unread(self):
        return self.model.query.filter_by(is_read=False).all()
    
    def mark_as_read(self, message):
        message.is_read = True
        self.commit()

