"""A GameController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller

from app.Table import Table
from app.User import User

from secrets import token_hex
from time import time 

def current_time():
    return int(time())

class GameController(Controller):
    """GameController Controller Class."""

    def __init__(self, request: Request):
        """GameController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request


    def show(self, view: View, request: Request):
        """
        Show all users so player can pick one user to play with
        """
        users = User.all()
        
        return view.render("game", {'users': users, 'name': request.user().name})
    
    def store(self, request: Request, view: View):
        """
        Generate a new token, return to chess/@token/ @show
        """
        friend = request.input('friend', clean=True)
        friend_id = User.where('name', friend).limit(1).first()

        if not friend_id:
            return 'Username is not exists'
        
        friend_id = friend_id.id 
       
        token = token_hex(16)
       
        Table.create(
            user_id = request.user().id,
            oppo_id = friend_id,
            token = token, 
            completed = False,
            last_move_timestamp = current_time(),
            next_id = request.user().id,
            move = '',
        )       
        return request.redirect("/play/@token", {'token': token})

    def resume(self, request: Request, view: View):
        token = request.input('token', clean=True)
        
        table = Table.where('token', token).limit(1).first()
        if not table:
            return "token is not exist"
        
        # Check timestamp
        timestamp = current_time() - table.last_move_timestamp
        
        if timestamp > 300: 
            table.completed = True
            return "Timeout"
        
        return request.redirect("/play/@token", {'token': token})



