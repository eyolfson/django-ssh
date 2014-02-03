# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import re
from subprocess import check_output, CalledProcessError, DEVNULL

from django import forms
from django.conf import settings
from django.db import IntegrityError

from eyl.django.ssh.models import Key

class KeyForm(forms.Form):
    file = forms.FileField()

    def __init__(self, user, *args, **kwargs):
        super(KeyForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_file(self):
        if self.user.ssh_keys.count() >= 5:
            message = 'Sorry, there is a maximum of 5 public keys.'
            raise forms.ValidationError(message, code='max_keys')

        f = self.cleaned_data['file']
        command = ['ssh-keygen', '-l', '-f', f.temporary_file_path()]
        try:
            output = check_output(command, stderr=DEVNULL)
        except CalledProcessError:
            message = 'Please submit a valid public key file.'
            raise forms.ValidationError(message, code='invalid')

        content = f.read().decode('utf-8')
        m = re.match('^\s*(\S+)\s+([0-9A-Za-z+/]+={,2})\s+(.*)', content)
        if not m:
            message = 'Unknown public key format.'
            raise forms.ValidationError(message, code='unknown')
        self.data = '{} {}'.format(m.group(1), m.group(2))
        self.comment = m.group(3).strip()

        m = re.match(b'^[0-9a-f]+\s+([0-9a-f]{2}(:[0-9a-f]{2}){15})', output)
        if not m:
            message = 'Unknown public key fingerprint.'
            raise forms.ValidationError(message, code='unknown')
        self.fingerprint = m.group(1).decode('utf-8')

        try:
            Key.objects.get(data=self.data)
            message = 'Sorry, this appears to be a duplicate public key.'
            raise forms.ValidationError(message, code='duplicate')
        except Key.DoesNotExist:
            pass

        return f

    def create(self):
        try:
            Key.objects.create(user=self.user, data=self.data,
                               comment=self.comment,
                               fingerprint=self.fingerprint)
        except IntegrityError:
            # There is a race condition where two forms with duplicate SSH
            # public keys may call create. The first create will succeed, but
            # the second will fail with an integrity error from the database.
            # In this case, just silently fail and let the user re-upload it
            # to get the proper error message.
            pass
