import tornado.web
from nbgrader.api import Gradebook

from .assignment import AssignmentHandler, AssignmentDetailHandler
from .handlers import NotFoundHandler
from tornado.log import gen_log

__all__ = ['Application']


class Application(tornado.web.Application):
    def __init__(self, db_url, **settings):
        if not settings.get('auth_token'):
            gen_log.info('Auth token not set. Authentication will be disabled!')

        self.gradebook = Gradebook(db_url)

        handlers = [
            (r'/assignments', AssignmentHandler),
            (r'/assignments/(.*)', AssignmentDetailHandler),
        ]

        default_settings = dict(
            default_handler_class=NotFoundHandler,
        )

        default_settings.update(**settings)

        super(Application, self).__init__(handlers, **default_settings)
