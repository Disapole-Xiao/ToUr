from django.db import models
from django.utils import timezone

from account.models import User
from travel.models import Destination

class Diary(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pub_time = models.DateTimeField(default=timezone.now, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    popularity = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True)
    location = models.ForeignKey(Destination, on_delete=models.PROTECT)

    def __str__(self):
        return f'title: {self.title} author: {self.author.username}'