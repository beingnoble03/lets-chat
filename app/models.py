from django.db import models
from datetime import datetime
from datetime import date
# Create your models here.

class Message(models.Model):
    username = models.CharField(max_length = 100)
    message = models.TextField()
    time = models.TimeField(default=datetime.now())
    date = models.DateField(default=date.today())
    first_name = models.CharField(default="Anonymous", max_length=100)
    last_name = models.CharField(default="", max_length=100)
    def __str__(self):
        return "%s : %s" % (self.message, self.username)
