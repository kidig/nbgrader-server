from tornado.web import RequestHandler


__all__ = ['BaseHandler', 'NotFoundHandler']


class BaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if not (self.settings.get("serve_traceback") and "exc_info" in kwargs):
            self.finish({'code': status_code, 'message': self._reason})
        else:
            super(BaseHandler, self).write_error(status_code, **kwargs)

    @property
    def gradebook(self):
        return self.application.gradebook

    def get_token_from_authorization_header(self):
        header_token = self.request.headers.get('Authorization')

        if header_token:
            token_type, header_token = str(header_token).split(' ')
            if token_type == 'Token' and header_token:
                return header_token

        return None


class NotFoundHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.send_error(404, reason='Not Found')

    def post(self, *args, **kwargs):
        self.get(*args, **kwargs)
