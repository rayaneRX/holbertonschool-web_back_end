#!/usr/bin/env python3
""" Basic Babel setup """

from flask import Flask, render_template, request, g
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """Config class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """ Get user from query parameter 'login_as' """
    user_id = request.args.get("login_as")
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """ Set user before each request if 'login_as' provided """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """ Get locale from URL parameter, user settings, or request header """
    # Locale from URL parameters
    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale

    # Locale from user settings
    user = getattr(g, 'user', None)
    if user is not None:
        user_locale = user.get('locale')
        if user_locale and user_locale in app.config["LANGUAGES"]:
            return user_locale

    # Locale from request header
    return request.accept_languages.best_match(app.config["LANGUAGES"])

# babel.init_app(app, locale_selector=get_locale)


@app.route("/", methods=["GET"])
def index():
    """ Index page """
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 