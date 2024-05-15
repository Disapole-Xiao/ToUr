from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


from account.models import User
from travel.models import Destination

class Diary(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pub_time = models.DateTimeField(default=timezone.now, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    popularity = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True, validators=[
            # 限制0~5
            MinValueValidator(0, message="Rating must be at least 0"),
            MaxValueValidator(5, message="Rating cannot be greater than 5"),
        ])
    location = models.ForeignKey(Destination, on_delete=models.PROTECT)

    def __str__(self):
        return f'title: {self.title} author: {self.author.username}'
    
class UserRating(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
            # 限制0~5
            MinValueValidator(0, message="Rating must be at least 0"),
            MaxValueValidator(5, message="Rating cannot be greater than 5"),
        ]
    )