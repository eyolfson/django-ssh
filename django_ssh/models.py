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
from re import match
from subprocess import check_output, CalledProcessError, DEVNULL
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

logger = getLogger('ssh')

class Key(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ssh_keys',
                             db_index=True)
    data = models.TextField(db_index=True, unique=True)
    comment = models.TextField(blank=True)
    fingerprint = models.CharField(max_length=47, blank=True)

    def clean(self):
        if not hasattr(settings, 'SSH_KEYS_MAX'):
            keys_max = settings.SSH_KEYS_MAX
        else:
            keys_max = 5
        if self.user.ssh_keys.count() >= keys_max:
            msg = 'You may only have a maximum of {} keys.'.format(keys_max)
            raise ValidationError(msg)
        with NamedTemporaryFile('w') as f:
            f.write('{}\n'.format(self.data))
            try:
                o = check_output(['ssh-keygen', '-l', '-f', f.name],
                                 stderr=DEVNULL, universal_newlines=True)
            except CalledProcessError:
                raise ValidationError('OpenSSH key data is not valid')
            m = match('[0-9]+ ([0-9a-f]{2}(:[0-9a-f]{2}){15})', o)
            if not m:
                msg = 'Unexpected OpenSSH key fingerprint'
                logger.error(msg)
                raise Exception(msg)
            self.fingerprint = m.group(1)

    class Meta:
        db_table = 'ssh_key'
