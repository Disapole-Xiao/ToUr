import os
from django.db import models

def dest_pic_path(instance, filename):
    # 生成一个新的文件名，保留原始文件的扩展名
    ext = filename.split('.')[-1]
    filename = f'{instance.name}.{ext}'
    # 返回存储的相对路径
    return os.path.join('destinations', filename)



class Destination(models.Model):
    name = models.CharField(max_length=50, unique=True)
    province = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=dest_pic_path, blank=True, null=True)
    popularity = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True)
    tags = models.TextField()  ## 可能还需要修改 空格分隔的标签

    def __str__(self):
        return self.name
