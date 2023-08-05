from flask import has_request_context


class ThrivveCore:
    """
    Singleton class for ThrivveCore
    """
    __app = None

    @staticmethod
    def get_app():
        """ Static access method. """
        if ThrivveCore.__app is None:
            ThrivveCore()
        return ThrivveCore.__app

    def __init__(self, app=None):
        """ Virtually private constructor. """
        if ThrivveCore.__app is not None:
            raise Exception("This class is a singleton!")
        else:
            ThrivveCore.__app = app
            _setup_default_routes(app)
            _setup_babel_locale(app)


def _setup_babel_locale(app):
    from flask import request, g
    from thrivve_core.helpers.auth import Auth
    babel = app.extensions['babel']

    @babel.localeselector
    def get_locale():
        """
        This function is used to determine the language to use for translations.
        """
        # if a user is logged in, use the locale from the user settings
        user = Auth.get_user()

        language = user.get('language')
        if language:
            return language
        # otherwise try to guess the language from the user accept
        # header the browser transmits. The best match wins.
        if not has_request_context():
            with app.test_request_context():
                with app.app_context():
                    return request.accept_languages.best_match(['ar', 'en'])
        else:
            with app.app_context():
                return request.accept_languages.best_match(['ar', 'en'])



def _setup_default_routes(app):
    from thrivve_core.app_decorators.app_entry import route
    from thrivve_core.helpers.fetch_relational_data import fetch_relational_data
    @route(
        path='/',
        require_auth=False
    )
    def _health_check_service():
        return dict(name="{} Service".format(app.config.get('SERVICE_NAME')), works=True)

    @route(
        path='/health_check',
        require_auth=False
    )
    def _health_check_with_path_service():
        return dict(name="{} Service".format(app.config.get('SERVICE_NAME')), works=True)

    @route("/fetch_relational_data", methods=["POST"], require_auth=False)
    def _fetch_relational_data_service(validated_data):
        """
        Swagger definition
        """
        user_data_key = '__user_auth_data__'
        if validated_data.get(user_data_key) is not None:
            from thrivve_core.helpers.auth import Auth
            Auth.set_user(validated_data.get(user_data_key))

        validated_data.pop(user_data_key)

        return fetch_relational_data(**validated_data)
