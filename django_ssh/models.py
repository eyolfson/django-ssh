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

from logging import getLogger

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

logger = getLogger('ssh')

class Key(models.Model):
    user = models.ForeignKey(User,
                             related_name='ssh_keys',
                             db_index=True)
    body = models.TextField(db_index=True, unique=True)
    comment = models.TextField(blank=True)
    fingerprint = models.CharField(max_length=47, blank=True)

    def clean(self):
        # Ensure that the maximum number of keys hasn't been reached
        if hasattr(settings, 'SSH_KEYS_MAX'):
            max_count = settings.SSH_KEYS_MAX
        else:
            max_count = 5
        if self.user.ssh_keys.count() >= max_count:
            msg = 'Reached the maximum number of keys ({})'.format(max_count)
            raise ValidationError(msg)

        # RFC 4253 Section 6.6
        from re import compile, ASCII
        key_re = compile('\s*([a-z][a-z-]*[a-z]) +([A-Za-z0-9+/=]+)(.*)', ASCII)
        fingerprint_re = compile('[0-9]+ ([0-9a-f]{2}(:[0-9a-f]{2}){15})')

        m = key_re.match(self.body)
        if not m:
            raise ValidationError('Invalid OpenSSH key.', code='invalid')
        self.body = '{} {}'.format(m.group(1), m.group(2))
        if self.comment == '':
            self.comment = m.group(3)
        self.comment = self.comment.strip()

        from subprocess import check_output, CalledProcessError, DEVNULL
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile('w') as f:
            f.write('{}\n'.format(self.body))
            f.flush()
            try:
                o = check_output(['ssh-keygen', '-l', '-f', f.name],
                                 stderr=DEVNULL, universal_newlines=True)
                m = fingerprint_re.match(o)
                if m:
                    self.fingerprint = m.group(1)
            except:
                raise ValidationError('Invalid OpenSSH key.', code='invalid')

    class Meta:
        db_table = 'ssh_key'
