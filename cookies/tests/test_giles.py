from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse

from cookies.giles import get_file_details, handle_giles_callback
from cookies.models import *

from social.apps.django_app.default.models import UserSocialAuth

import unittest, mock, json
from collections import Counter


class MockResponse(object):
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def json(self):
        return json.loads(self.content)


def mock_get_fileids(url, params={}, headers={}):
    with open('cookies/tests/data/giles_file_response.json', 'r') as f:
        return MockResponse(200, f.read())


class TestGiles(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='nope',
        )
        self.auth = UserSocialAuth.objects.create(**{
            'user': self.user,
            'provider': 'github',
            'uid': 'asdf1234',
        })
        self.auth.extra_data['access_token'] = 'fdsa5432'
        self.auth.save()

        self.page_field = Field.objects.create(uri='http://xmlns.com/foaf/0.1/page')
        self.part_type = Type.objects.create(uri='http://purl.org/net/biblio#Part')
        self.image_type = Type.objects.create(uri='http://xmlns.com/foaf/0.1/Image')
        self.document_type = Type.objects.create(uri='http://xmlns.com/foaf/0.1/Document')

    def test_get_file_details(self):
        request = self.factory.get(reverse('create-handle-giles') + '?uploadids=asdf1234')
        request.user = self.user

        get = mock.Mock(side_effect=mock_get_fileids)
        result = get_file_details(request, 'asdf1234', get=get)

        self.assertEqual(get.call_count, 1)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 3)

    def test_handle_giles_callback(self):
        get = mock.Mock(side_effect=mock_get_fileids)
        request = self.factory.get(reverse('create-handle-giles') + '?uploadids=asdf1234')
        request.user = self.user

        session = handle_giles_callback(request, get=get)
        self.assertEqual(get.call_count, 1)
        self.assertIsInstance(session, GilesSession)
        self.assertEqual(len(session.file_details), 3)

        self.assertEqual(session.content_resources.count(), 4)
        self.assertEqual(session.resources.count(), 3)

        def _try_related(obj, prop):
            try:
                getattr(obj, prop)
                return True
            except:
                return False

        types = Counter()
        for resource in session.resources.all():
            types[resource.entity_type.id] += 1
            if resource.entity_type == self.image_type:
                self.assertIsInstance(resource.content.first().content_resource,
                                      Resource)
            elif resource.entity_type == self.document_type:
                self.assertEqual(resource.content.count(), 0)
                self.assertEqual(resource.relations_from.count(), 2)
                for relation in resource.relations_from.all():
                    self.assertEqual(relation.predicate, self.page_field)
                    target = relation.target
                    self.assertIsInstance(target, Resource)
                    self.assertEqual(target.entity_type, self.part_type)
                    self.assertTrue(_try_related(target, 'next_page') or _try_related(target, 'previous_page'))


    def tearDown(self):
        # Prevent unique constraint violation.
        self.user.delete()
        self.page_field.delete()
        self.part_type.delete()
        self.image_type.delete()
        self.document_type.delete()
        self.auth.delete()


if __name__ == '__main__':
    unittest.main()