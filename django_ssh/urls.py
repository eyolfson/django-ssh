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

from django.urls import path

from django_ssh import views

app_name = 'ssh'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-file/', views.add_file, name='add-file'),
    path('add-text/', views.add_text, name='add-text'),
    path('remove-<int:key_id>/', views.remove, name='remove'),
]
