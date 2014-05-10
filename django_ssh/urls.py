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

from django.conf.urls import url

from django_ssh import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add-file/$', views.add_file, name='add-file'),
    url(r'^add-text/$', views.add_text, name='add-text'),
    url(r'^remove-(?P<key_id>\d+)/$', views.remove, name='remove'),
]
