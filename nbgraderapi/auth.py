import tornado.web
import functools


def token_required(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        token = self.get_token_from_authorization_header()

        if not token:
            raise tornado.web.HTTPError(401, 'Unauthorized Access. Token is missing.')

        auth_token = self.application.settings.get('auth_token')

        if auth_token and not token == auth_token:
            raise tornado.web.HTTPError(403, 'Auth token invalid.')

        return method(self, *args, **kwargs)
    return wrapper
