"""Table Model."""

from config.database import Model
from orator.orm import belongs_to

class Table(Model):
    """Table Model."""
    __fillable__ = ['user_id', 'oppo_id', 'token', 'move', 'completed', 'last_move_timestamp', 'next_id', 'owner']
    __table__ = 'chesses'

    @belongs_to('user_id', 'email')
    def user(self):
        from app.User import User 
        return User
