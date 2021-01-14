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

from distutils.core import setup

setup(
    name = 'django-ssh',
    packages = ['django_ssh'],
    version = '0.2.1',
    description = 'A basic Django app for storing SSH keys',
    author = 'Jon Eyolfson',
    author_email = 'jon@eyl.io',
    url = 'https://github.com/eyolfson/django-ssh/',
    license = 'COPYING',
    download_url = ('https://github.com/eyolfson/django-ssh/archive/'
                    'v0.2.1.tar.gz'),
    classifiers = [
        'Framework :: Django',
        ('License :: OSI Approved :: GNU General Public License v3 or later '
         '(GPLv3+)'),
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
    ],
)
