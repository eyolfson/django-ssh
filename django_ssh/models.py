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
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

logger = getLogger('ssh')

class OpenSSHBodyField(models.TextField):

    def __init__(self, *args, **kwargs):
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        if 'unique' not in kwargs:
            kwargs['unique'] = True
        super(OpenSSHBodyField, self).__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super(OpenSSHBodyField, self).validate(value, model_instance)
        from subprocess import call, DEVNULL
        with NamedTemporaryFile('w') as f:
            f.write('{}\n'.format(value))
            f.flush()
            rc = call(['ssh-keygen', '-l', '-f', f.name], stdout=DEVNULL,
                      stderr=DEVNULL)
        if rc != 0:
            raise ValidationError('Invalid OpenSSH key', code='invalid')

class Key(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='ssh_keys',
                             db_index=True)
    body = OpenSSHBodyField()
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

        # Calculate the fingerprint
        from subprocess import check_output, CalledProcessError, DEVNULL
        from re import match
        with NamedTemporaryFile('w') as f:
            f.write('{}\n'.format(self.body))
            f.flush()
            try:
                o = check_output(['ssh-keygen', '-l', '-f', f.name],
                                 stderr=DEVNULL, universal_newlines=True)
                m = match('[0-9]+ ([0-9a-f]{2}(:[0-9a-f]{2}){15})', o)
                if m:
                    self.fingerprint = m.group(1)
            except CalledProcessError:
                pass

    class Meta:
        db_table = 'ssh_key'
