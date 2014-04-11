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

    def test_add_text_valid(self):
        body = ('ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHmrZYaqcFtZhbvYVINLVbWV'
                'I8ig4mLqYdzCDIC7uAlnFdOAMsEuSK0zW0CrRQ+19TAPNasm284hqXD7N+nylb'
                '8y75BWiUhxh+IK68oxexXdAwpQEKg7pX7PB+GuYF7z6zqsubDsOxL3jx/pZNTY'
                'fNXTuzYfrfhw83lXxRml75x789pFjg9D0D/Bc/yB6sfd8kvFu+vkt/TXmcsvzB'
                'tw7AA3J58EIy9nuxon7aDdnwTVkS7DLhBLU/UWXMlkxHHEAL1E+6uxvyCfINrI'
                '15kkaiY68/46NWrXSHPmHouBoZnQxYMEkmAd12OMIkilAsS6LxGoAB4ABOuQWQ'
                'epT3kayn')
        comment = 'u1 k1'
        fingerprint = 'c6:35:81:1c:a3:ed:9b:2b:36:9f:04:27:13:05:85:10'
        self.assertTrue(self.client.login(username='u1', password='p1'))
        response = self.client.post('/add-text/', {'body': body})
        self.assertRedirects(response, '/')
        self.assertEquals(self.u1.ssh_keys.count(), 1)
        self.assertEquals(self.u1.ssh_keys.all()[0].fingerprint, fingerprint)

    def test_add_text_invalid(self):
        self.assertTrue(self.client.login(username='u1', password='p1'))
        response = self.client.post('/add-text/', {'body': 'INVALID'})
        self.assertFormError(response, 'form', 'body', 'Enter a valid SSH key.')
