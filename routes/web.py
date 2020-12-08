"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),
    
    Get('/game', 'GameController@show'),
    Get('/game/create', 'GameController@store'),
    Get('/game/resume', 'GameController@resume'),
]

from masonite.auth import Auth 
ROUTES += Auth.routes()
