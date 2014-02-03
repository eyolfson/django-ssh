# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.db import models

class Key(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ssh_keys',
                             db_index=True)
    data = models.TextField(db_index=True, unique=True)
    comment = models.TextField()
    fingerprint = models.CharField(max_length=47)
