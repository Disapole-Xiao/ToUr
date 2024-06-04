from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.core.cache import cache

from travel.models import Destination
from src.compress import compress, decompress

User = get_user_model()

class Diary(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pub_time = models.DateTimeField(default=timezone.now, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    content_compressed = models.BinaryField(blank=True, null=True)
    popularity = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True, validators=[
            # 限制0~5
            MinValueValidator(0, message="Rating must be at least 0"),
            MaxValueValidator(5, message="Rating cannot be greater than 5"),
        ])
    location = models.ForeignKey(Destination, on_delete=models.PROTECT)

    def is_compressed(self) -> bool:
        return self.content_compressed != None
    is_compressed.boolean = True
    def get_content(self):
        if self.is_compressed():
            content = cache.get(f'diary_{self.id}_content')
            if content == None:
                content = decompress(self.content_compressed)
                cache.set(f'diary_{self.id}_content', content)
            return content
        else:
            return self.content
    def __str__(self):
        if self.author:
            return f'title: {self.title} author: {self.author.username}'
        else:
            return f'title: {self.title} author: None'  
    def save(self, *args, **kwargs):
        # 如果是创建对象
        # if self.pk == None:
        if self.content != None:
            # 压缩content，与压缩前比较大小决定是否要压缩
            compressed, ratio = compress(self.content)
            if ratio > 1.1:
                self.content_compressed = compressed
                self.content = None
                print(f'日记 "{self.title}" 压缩成功，压缩率 {ratio}')
            else:
                self.content_compressed = None
            
        super(Diary, self).save(*args, **kwargs)

class UserRating(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
            # 限制0~5
            MinValueValidator(0, message="Rating must be at least 0"),
            MaxValueValidator(5, message="Rating cannot be greater than 5"),
        ]
    )