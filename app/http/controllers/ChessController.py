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

        # Non exist token
        if not table:
            return view.render("invalid", {"message": 'Your Token is not existed'})

        if not request.user():
            return view.render("invalid", {"message": 'Please login first'})

        # Exist token, but no permission
        if request.user().email not in (table.user_id, table.oppo_id):
            return view.render("invalid", {"message": 'You cannot view this game'})

        if current_time() - table.last_move_timestamp > 300:
            table.completed = True
            table.save()
            return view.render("invalid", {"message": 'Time out'})

        # If everything okay, print out current move of this game
        timeleft = 300 - (current_time() - table.last_move_timestamp)
        your_turn = table.next_id == request.user().email

        return view.render('chess', {'table': table, 'your_turn': your_turn, 'timeleft': timeleft})

    def move(self, request: Request, view: View):
    # Input move in the game, turn base so we have to check
        token = request.param('token')

        table = Table.where('token', token).limit(1).first()

        if not table:
            return view.render("invalid", {"message": 'Your Token is not existed'})

        # Check time out
        if table.completed:
            return view.render("invalid", {"message": 'Time out'})


        if table.next_id != request.user().email:
            return view.render("invalid", {"message": 'Please wait for your turn'})

        # Update game
        move = request.input('move')
        table.move += request.input('move')

        if table.next_id == table.user_id:
            # Turn A
            table.next_id = table.oppo_id
        elif table.next_id == table.oppo_id:
            # Turn B
            table.next_id = table.user_id

        table.last_move_timestamp = current_time()

        table.save()

        # TODO: update game in game functionalities

        return request.redirect('/play/@token', {'token': token})
