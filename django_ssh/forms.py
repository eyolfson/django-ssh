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

import re

from subprocess import check_output, CalledProcessError, DEVNULL

from django import forms
from django.conf import settings
from django.db import IntegrityError

from django_ssh.models import Key

class KeyFileForm(forms.Form):
    file = forms.FileField()

class KeyTextForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea)
    comment = forms.CharField(required=False)
