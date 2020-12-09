"""A ChessController Module."""

from app.http.controllers.GameController import current_time
from app.Table import Table
from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
from app.http.controllers.game.game import chinesechess
import string


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

        if not request.user():
            return view.render("invalid", {"message": 'Please login first'})

        # Non exist token
        if not table:
            return view.render("invalid", {"message": 'Your Token is not existed'})

        # Exist token, but no permission
        if request.user().email not in (table.user_id, table.oppo_id):
            return view.render("invalid", {"message": 'You cannot view this game'})

        # Check time out
        if table.completed:
            return view.render("invalid", {"message": 'Time out'})

        if current_time() - table.last_move_timestamp > 300:
            table.completed = True
            table.save()
            return view.render("invalid", {"message": 'Time out'})

        # If everything okay, print out current move of this game
        timeleft = 300 - (current_time() - table.last_move_timestamp)
        your_turn = table.next_id == request.user().email

        return view.render('chess', {'table': table, 'your_turn': your_turn, 'timeleft': timeleft})

    def move(self, request: Request, view: View):
        token = request.param('token')

        if not request.user():
            return view.render("invalid", {"message": 'Please login first'})

        table = Table.where('token', token).limit(1).first()

        # Check token exist
        if not table:
            return view.render("invalid", {"message": 'Your Token is not existed'})

        # Exist token, but no permission
        if request.user().email not in (table.user_id, table.oppo_id):
            return view.render("invalid", {"message": 'You cannot view this game'})

        # Check time out
        if table.completed:
            return view.render("invalid", {"message": 'Time out'})

        # Turn base constrain
        if table.next_id != request.user().email:
            return view.render("invalid", {"message": 'Please wait for your turn'})

        
        # Clean up space
        move = request.input('move')
        move = move.strip().lstrip()
        
        if not all(i in (string.ascii_letters + string.digits) for i in  move):
            return view.render('invalid', {"message": "Please enter valid move"})

        moves = table.move + move

        code, msg = chinesechess(moves)
        if code == -1: 
            # Illegal move
            table.msg = 'Illegal move'
            return view.render('invalid', {"message": msg})
        elif code == 0:
            # Black win
            table.winner = table.next_id
            table.completed = True
        elif code == 1:
            # Red win
            table.winner = table.next_id
            table.completed = True
        elif code == 2:
            # Draw
            table.winner = 'Draw'
            table.completed = True
        else:
            # Legal move
            table.msg = msg

        table.move = moves

        if table.next_id == table.user_id:
            # Turn A
            table.next_id = table.oppo_id
        elif table.next_id == table.oppo_id:
            # Turn B
            table.next_id = table.user_id

        table.last_move_timestamp = current_time()

        table.save()

        return request.redirect('/play/@token', {'token': token})
