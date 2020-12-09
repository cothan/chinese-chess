"""A ChessController Module."""

from app.http.controllers.GameController import current_time
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
        
        table = Table.where('token', token).limit(1).first()
        if not table:
            return "Token is not exists"
        
        if current_time() - table.last_move_timestamp > 300: 
            table.completed = True
            table.save()

        print('============', table.completed)
        return view.render('chess', {'table': table})

    def move(self, request: Request, view: View):
        # Input move in the game, turn base so we have to check
        token = request.param('token')

        table = Table.where('token', token).limit(1).first()

        if not table:
            return "Token is not exists"

        # Check time out 
        if table.completed:
            return "Time out"

        if table.next_id != request.user().id:
            return "Not your turn"
        
        # Update game 
        table.next_id = table.oppo_id
        move = request.input('move')
        print(move, '===========', table.move)
        table.move += request.input('move')

        table.save()

        # TODO: update game in game functionalities

        return request.redirect('/play/@token', {'token': token})
    