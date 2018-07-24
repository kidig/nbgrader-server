import tornado.web
import functools


def token_required(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        auth_token = self.application.settings.get('auth_token')

        if auth_token:
            token = self.get_token_from_authorization_header()

            if not token:
                raise tornado.web.HTTPError(401, 'Unauthorized access. Token is missing.')

            if not token == auth_token:
                raise tornado.web.HTTPError(403, 'Invalid token.')

        return method(self, *args, **kwargs)
    return wrapper
