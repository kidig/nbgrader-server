import urllib

from tornado.escape import json_decode
from tornado.testing import AsyncHTTPTestCase

from nbgraderapi import Application


class TestHandlerBase(AsyncHTTPTestCase):
    def get_app(self):
        return Application(db_url='sqlite:///:memory:', auth_token='testing-token')

    def get_token_auth_headers(self, auth_token=None):
        if not auth_token:
            auth_token = self._app.settings['auth_token']
        return {
            'Authorization': 'Token {}'.format(auth_token)
        }

    def fetch_json(self, *args, **kwargs):
        response = self.fetch(*args, **kwargs)
        response.rethrow()
        return json_decode(response.body)


class TestAssignmentHandler(TestHandlerBase):

    def setUp(self):
        super(TestAssignmentHandler, self).setUp()
        app = self._app
        app.gradebook.add_assignment('bar')
        app.gradebook.add_assignment('foo')

    def test_auth(self):
        response = self.fetch('/assignments')
        self.assertEqual(response.code, 401)

    def test_bad_token(self):
        response = self.fetch('/assignments', headers=self.get_token_auth_headers('bad-token'))
        self.assertEqual(response.code, 403)

    def test_assignment_list(self):
        data = self.fetch_json(
            '/assignments',
            headers=self.get_token_auth_headers(),
        )
        self.assertEqual(len(data['items']), 2)
        self.assertDictContainsSubset({'name': 'bar'}, data['items'][0])
        self.assertDictContainsSubset({'name': 'foo'}, data['items'][1])

    def test_assignment_create(self):
        response = self.fetch(
            '/assignments',
            method='POST',
            body=urllib.urlencode({'name': 'one'}),
            headers=self.get_token_auth_headers(),
        )
        self.assertEqual(response.code, 204)

        app = self._app
        assignment = app.gradebook.find_assignment('one')
        self.assertIsNotNone(assignment)
