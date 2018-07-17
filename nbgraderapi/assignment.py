from .handlers import BaseHandler
from .auth import token_required
import tornado.web

__all__ = ['AssignmentHandler', 'AssignmentDetailHandler']


class AssignmentListMixin(object):
    def list(self, *args, **kwargs):
        items = [i.to_dict() for i in self.gradebook.assignments]
        self.write({'items': items})


class AssignmentRetrieveMixin(object):
    def retrieve(self, name):
        obj = self.gradebook.find_assignment(name)
        self.write(obj.to_dict())


class AssignmentCreateMixin(object):
    def create(self, *args, **kwargs):
        name = self.get_argument('name')
        if not name:
            self.send_error(400, reason='name is required')

        assignment = self.gradebook.add_assignment(name)
        if assignment:
            self.set_status(204)
            self.finish()


class AssignmentRemoveMixin(object):
    def remove(self, name, *args, **kwargs):
        self.gradebook.remove_assignment(name)
        self.set_status(204)
        self.finish()


class AssignmentHandler(AssignmentListMixin, AssignmentCreateMixin, BaseHandler):
    @token_required
    def get(self, *args, **kwargs):
        self.list(*args, **kwargs)

    @token_required
    def post(self, *args, **kwargs):
        self.create(*args, **kwargs)


class AssignmentDetailHandler(AssignmentRetrieveMixin, AssignmentRemoveMixin, BaseHandler):
    @token_required
    def get(self, *args, **kwargs):
        self.retrieve(*args, **kwargs)

    @token_required
    def delete(self, *args, **kwargs):
        self.remove(*args, **kwargs)