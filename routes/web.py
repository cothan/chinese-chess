"""Web Routes."""

from masonite.auth import Auth
from masonite.routes import Get, Post

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),

    Get('/game', 'GameController@show'),
    Post('/game/create', 'GameController@store'),
    # Post('/game/resume', 'GameController@resume'),

    Get('/play/@token', 'ChessController@show'),
    Post('/play/@token/move', 'ChessController@move')
]

ROUTES += Auth.routes()
