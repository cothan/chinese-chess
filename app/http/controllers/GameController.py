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
        table = Table.all()
        
        if request.user():
            cur_user = request.user().email
            return view.render("game", {'users': users, 'name': cur_user, 'table': table, "cuser_id" : cur_user} )
        else:
            return view.render("invalid", {"message": 'Please log in'})


    def store(self, request: Request, view: View):
        """
        Generate a new token, return to chess/@token/ @show
        """
        cur_user = request.user()

        friend = request.input('friend', clean=True).strip()
        friend_email = User.where('email', friend).limit(1).first()

        if not friend_email:
            return view.render("invalid", {"message": 'Username is not exists'})

        friend_email = friend_email.email
        user_email = cur_user.email

        if friend_email == user_email:
            return view.render("invalid", {"message": 'You cannot play alone'})

        token = token_hex(16)

        Table.create(
            owner  = user_email,
            user_id=user_email,
            oppo_id=friend_email,
            token=token,
            completed=False,
            last_move_timestamp=current_time(),
            next_id=user_email,
            move='',
        )
        return request.redirect("/play/@token", {'token': token})


    # def resume(self, request: Request, view: View):
    #     token = request.input('token', clean=True).strip()

    #     table = Table.where('token', token).limit(1).first()
    #     print(table, '===========')
    #     if not table:
    #         return "token is not exist"

    #     # Check timestamp
    #     timestamp = current_time() - table.last_move_timestamp

    #     if timestamp > 300:
    #         table.completed = True
    #         table.save()
    #         return view.render("invalid", {"message": "Time Out"})

    #     return request.redirect("/play/@token", {'token': token})
