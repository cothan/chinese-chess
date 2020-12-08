"""A ChessController Module."""

from app.Table import Table
from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller


class ChessController(Controller):
    """ChessController Controller Class."""

    def __init__(self, request: Request):
        """ChessController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View, request: Request):
        # Show move in the game 
        token = request.param('token')
        
        table = Table.find(token)

        return view.render('chess', {'table': table})

    def move(self, request: Request):
        # Input move in the game, turn base so we have to check
        token = request.param('token')

        table = Table.find(token)

        if table.next_id != request.user().id:
            return "Not your turn"
        
        # Update game 
        table.next_id = table.oppo_id

        # TODO: update game in game functionalities

        return request.redirect('/play/@token', {'token': token})
    