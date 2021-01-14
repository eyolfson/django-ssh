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

from tempfile import NamedTemporaryFile

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class BasicTestCase(TestCase):

    def setUp(self):
        self.u1 = User.objects.create_user('u1', password='p1')
        self.u2 = User.objects.create_user('u2', password='p2')
        self.k1 = {'format': 'ssh-rsa',
                   'data': (
                       'AAAAB3NzaC1yc2EAAAADAQABAAABAQDHmrZYaqcFtZhbvYVINLVbWVI'
                       '8ig4mLqYdzCDIC7uAlnFdOAMsEuSK0zW0CrRQ+19TAPNasm284hqXD7'
                       'N+nylb8y75BWiUhxh+IK68oxexXdAwpQEKg7pX7PB+GuYF7z6zqsubD'
                       'sOxL3jx/pZNTYfNXTuzYfrfhw83lXxRml75x789pFjg9D0D/Bc/yB6s'
                       'fd8kvFu+vkt/TXmcsvzBtw7AA3J58EIy9nuxon7aDdnwTVkS7DLhBLU'
                       '/UWXMlkxHHEAL1E+6uxvyCfINrI15kkaiY68/46NWrXSHPmHouBoZnQ'
                       'xYMEkmAd12OMIkilAsS6LxGoAB4ABOuQWQepT3kayn'),
                   'fingerprint':
                       'c6:35:81:1c:a3:ed:9b:2b:36:9f:04:27:13:05:85:10'}
        self.k2 = {'format': 'ssh-rsa',
                   'data': (
                       'AAAAB3NzaC1yc2EAAAADAQABAAABAQCz5qmlFdgVv5waCl9XqrRLBpk'
                       'fv/G8mTveYNhaLrLy34NreDSMPqK0qsX4qAn7gl+Aixvj9F4LONidxp'
                       'wrG+gaMVKQ7yHS9oiqQk6YXYmQMI0Pe4dB6kEj3bDgThxNh8D2kgD6C'
                       'EHROzkeXhsj3Z3e3vCqulzhmgYHHesKKnVQKrt38/WTEeeoYKfQGRgZ'
                       'RjUHurQlDZN0y65Ohh5zyH1jtQ4TMFUwtWsmKZZVVhA1HnsWF8mcSUo'
                       'RhaOECHreMy9f8qNXsZypM6032rM5GMBsrRv3JT/77kGnHSM1GIPN7r'
                       'wIeXgDttffWMIrjiodT7j7gq1ZON93RBeu5QGgzHo9'),
                   'fingerprint':
                       '51:ca:91:01:0f:14:7b:1a:d9:81:28:d7:9b:46:bb:2a'}

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(username='u1', password='p1'))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_text_basic(self):
        body = '{format} {data}'.format(**self.k1)
        comment = 'u1 k1'
        fingerprint = self.k1['fingerprint']
        self.assertTrue(self.client.login(username='u1', password='p1'))
        response = self.client.post('/add-text/', {'body': body,
                                                   'comment': comment})
        self.assertRedirects(response, '/')
        self.assertEquals(self.u1.ssh_keys.count(), 1)
        self.assertEquals(self.u1.ssh_keys.get().fingerprint, fingerprint)

    def test_add_text_body_with_comment(self):
        body = '{format} {data} u1 k1'.format(**self.k1)
        self.assertTrue(self.client.login(username='u1', password='p1'))
        response = self.client.post('/add-text/', {'body': body})
        self.assertRedirects(response, '/')
        self.assertEquals(self.u1.ssh_keys.count(), 1)
        self.assertEquals(self.u1.ssh_keys.get().comment, 'u1 k1')

    def test_add_file_valid(self):
        comment = 'u1 k2'
        fingerprint = self.k2['fingerprint']
        self.assertTrue(self.client.login(username='u1', password='p1'))
        with NamedTemporaryFile('bw+') as f:
            f.write(self.k2['format'].encode())
            f.write(b' ')
            f.write(self.k2['data'].encode())
            f.write(b' ')
            f.write(comment.encode())
            f.write(b'\nEXTRA')
            f.flush()
            f.seek(0)
            response = self.client.post('/add-file/', {'file': f})
        self.assertRedirects(response, '/')
        self.assertEquals(self.u1.ssh_keys.count(), 1)
        self.assertEquals(self.u1.ssh_keys.get().fingerprint, fingerprint)
        self.assertEquals(self.u1.ssh_keys.get().comment, comment)

    def test_add_text_invalid(self):
        self.assertTrue(self.client.login(username='u1', password='p1'))
        response = self.client.post('/add-text/', {'body': ''})
        self.assertFormError(response, 'form', 'body', 'This field is required.')
        response = self.client.post('/add-text/', {'body': 'INVALID'})
        self.assertFormError(response, 'form', None, 'Invalid OpenSSH key.')
