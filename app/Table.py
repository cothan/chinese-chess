"""Table Model."""

from config.database import Model
from orator.orm import belongs_to

class Table(Model):
    """Table Model."""
    __fillable__ = ['user_id', 'oppo_id', 'game_id', 'move', 'completed', 'last_move_timestamp']

    @belongs_to('user_id', 'id')
    def user(self):
        from app.User import User 
        return User
