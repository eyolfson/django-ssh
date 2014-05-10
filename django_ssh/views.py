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

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from django_ssh.forms import KeyFileForm, KeyTextForm
from django_ssh.models import Key

@login_required
def index(request):
    return render(request, 'ssh/index.html',
                  {'keys': Key.objects.filter(user=request.user)})

@login_required
def add_file(request):
    if request.method == 'POST':
        form = KeyFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            key = Key(user=request.user, body=file.read().decode())
            try:
                key.full_clean()
                key.save()
                return redirect('ssh:index')
            except ValidationError as e:
                for field, error_list in e.error_dict.items():
                    for error in error_list:
                        form.add_error(None, error)
    else:
        form = KeyFileForm()
    return render(request, 'ssh/add_file.html', {'form': form})

@login_required
def add_text(request):
    if request.method == 'POST':
        form = KeyTextForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            comment = form.cleaned_data['comment']
            key = Key(user=request.user, body=body, comment=comment)
            try:
                key.full_clean()
                key.save()
                return redirect('ssh:index')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = KeyTextForm()
    return render(request, 'ssh/add_text.html', {'form': form})

@login_required
def remove(request, key_id):
    try:
        key = Key.objects.get(pk=key_id, user=request.user)
        key.delete()
    except Key.DoesNotExist:
        pass
    return redirect('ssh:index')
