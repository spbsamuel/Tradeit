from __future__ import unicode_literals

from django.db import models

# Create your models here.
class BotUser(models.Model):
    joined = models.DateTimeField()
    last_activity = models.DateTimeField()
    fb_user_id = models.TextField(unique=True)
    location = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    last_state = models.IntegerField(default=0)
    profile_pic = models.URLField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10,choices=[
        ('male','male'),
        ('female','female')
    ])

    def __unicode__(self):
        return self.first_name + " " + self.last_name

class Item(models.Model):
    owner = models.ForeignKey(BotUser)
    image_url =models.URLField(null=True)
    description = models.TextField(null=True)
    active = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    accept_count = models.IntegerField(default=0)
    reject_count = models.IntegerField(default=0)
    date_created = models.DateTimeField()
    last_active = models.DateTimeField(null=True)
    is_editing = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description

class Match(models.Model):
    item_A = models.ForeignKey(Item,related_name="a_item")
    item_B = models.ForeignKey(Item,related_name="b_item")
    user_A_response = models.TextField()
    user_B_response = models.TextField()
    user_A_timespent = models.FloatField()
    user_B_timespent = models.FloatField()
    status = models.CharField(max_length=255)
    datetime = models.DateTimeField()

    def __unicode__(self):
        return str(self.item_A) + " - " + str(self.item_B)

class Log(models.Model):
    user = models.ForeignKey(BotUser)
    datetime = models.DateTimeField()
    json_text = models.TextField()


