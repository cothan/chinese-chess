"""A GameController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller

from app.Table import Table
from app.User import User

from secrets import token_hex
from time import time 

class GameController(Controller):
    """GameController Controller Class."""

    def __init__(self, request: Request):
        """GameController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request


    def show(self, view: View):
        """
        Show all users so player can pick one user to play with
        """
        users = User.all()
        
        return view.render("game", {'users': users})
    
    def store(self, request: Request, view: View):
        """
        Generate a new game_id, return to chess/@game_id/ @show
        """
        friend = request.input('friend')
        # TODO: filter friend input 
        if not User.find(friend):
            return 'Invalid username'
        friend_id = User.find(friend).id 
        token = token_hex(16)
        Table.create(
            user_id = request.user().id,
            oppo_id = friend_id,
            game_id = token, 
            completed = False,
            last_move_timestamp = int(time),
        )       
        return view.render(f'play/{token}')

    def resume(self, request: Request, view: View):
        game_id = request.input('game_id')
        #TODO: filter game_id 
        
        table = Table.find(game_id)
        if not table:
            return "game_id is not exist"
        
        # Check timestamp
        timestamp = int(time) - table.last_move_timestamp
        
        if timestamp > 300: 
            table.completed = True
            return "Timeout"
        

        return view.render(f'play/{game_id}')



