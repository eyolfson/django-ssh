# Copyright 2014 Jon Eyolfson
#
# This file is part of Django SSH.
#
# Django SSH is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Django SSH is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Django SSH. If not, see <http://www.gnu.org/licenses/>.

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import Client, TestCase

from django_ssh.models import SSHKeyBodyField

class BasicTestCase(TestCase):

    def setUp(self):
        self.u1 = User.objects.create_user('u1', password='p1')
        self.u2 = User.objects.create_user('u2', password='p2')

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(username='u1', password='p1'))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_text_invalid(self):
        self.assertTrue(self.client.login(username='u1', password='p1'))
        response = self.client.post('/add-text/', {'body': 'INVALID'})
        self.assertFormError(response, 'form', 'body', 'Enter a valid SSH key.')
