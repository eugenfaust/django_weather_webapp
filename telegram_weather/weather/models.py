from django.db import models


class Users(models.Model):
    status = models.BooleanField(blank=True, null=True)
    uid = models.BigIntegerField(unique=True, blank=True, null=True)
    admin = models.BooleanField(blank=True, null=True)
    last_action = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    city_name = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    ref_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
