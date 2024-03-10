#!/usr/bin/env python3
""" Basic Babel setup """
from flask import Flask, render_template, g, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """ Configuration Babel """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@app.route("/", methods=['GET'])
def index():
    """
    Rendre le modèle avec les informations utilisateur appropriées
    """
    return render_template('5-index.html')


def get_user() -> dict:
    """Retrieve user based on login_as parameter"""
    user_id = request.args.get('login_as')
    try:
        user_id = int(user_id)
        if user_id in users:
            return users[user_id]
    except (ValueError, TypeError):
        pass
    return None


@app.before_request
def before_request():
    """
    Définir l'utilisateur global s'il est connecté
    """
    user = get_user()
    if user:
        g.user = user


@babel.localeselector
def get_locale():
    """
    Déterminer la langue préférée de l'utilisateur
    """
    requested_locale = request.args.get('locale')
    if requested_locale in Config.LANGUAGES:
        return requested_locale

    return request.accept_languages.best_match(Config.LANGUAGES)
