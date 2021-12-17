from django.db   import models

from core.models import TimeStamp


class User(TimeStamp):
    nickname     = models.CharField(max_length=32)
    password     = models.CharField(max_length=128)
    is_admin     = models.BooleanField(default=False)


    class Meta:
        db_table = "users"