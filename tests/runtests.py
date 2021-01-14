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

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == '__main__':
    settings.configure(INSTALLED_APPS = (
                           'django.contrib.contenttypes',
                           'django.contrib.sessions',
                           'django.contrib.auth',
                           'django_ssh',
                       ),
                       ROOT_URLCONF = 'urls',
                       MIDDLEWARE = [
                           'django.contrib.sessions.middleware.SessionMiddleware',
                           'django.contrib.auth.middleware.AuthenticationMiddleware',
                       ],
                       TEMPLATES = [
                           {
                               'BACKEND': 'django.template.backends.django.DjangoTemplates',
                               'DIRS': [],
                               'APP_DIRS': True,
                               'OPTIONS': {
                               },
                           },
                       ],
                       DATABASES = {
                           'default': {
                               'ENGINE': 'django.db.backends.sqlite3'
                           },
                       })
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    test_runner.run_tests(['django_ssh'])
