"""The RegisterController Module."""

from masonite.auth import Auth, MustVerifyEmail
from masonite.managers import MailManager
from masonite.request import Request
from masonite.validation import Validator
from masonite.view import View

from app.User import User


class RegisterController:
    """The RegisterController class."""

    def __init__(self):
        """The RegisterController Constructor."""
        pass

    def show(self, view: View):
        """Show the registration page.

        Arguments:
            Request {masonite.request.request} -- The Masonite request class.

        Returns:
            masonite.view.View -- The Masonite View class.
        """
        return view.render("auth/register")

    def store(
        self,
        request: Request,
        mail_manager: MailManager,
        auth: Auth,
        validate: Validator,
    ):
        """Register the user with the database.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        errors = request.validate(
            validate.required(["name", "email", "password"]),
            validate.email("email"),
            validate.strong(
                "password",
                length=1,
                special=0,
                uppercase=0,
                # breach=True checks if the password has been breached before.
                # Requires 'pip install pwnedapi'
                breach=False,
            ),
        )
        if User.where('email', request.input("email")).limit(1).first():
            print('error', errors)
            errors.merge({'email': ["Email was used by someone else"]})
            print('error', errors)
            # return request.back().with_errors(errors).with_input()

        if errors:
            return request.back().with_errors(errors).with_input()

        user = auth.register(
            {
                "name": request.input("name"),
                "password": request.input("password"),
                "email": request.input("email"),
            }
        )

        if isinstance(user, MustVerifyEmail):
            user.verify_email(mail_manager, request)

        # Login the user
        if auth.login(request.input("email"), request.input("password")):
            # Redirect to the homepage
            return request.redirect("/home")

        # Login failed. Redirect to the register page.
        return request.back().with_input()
