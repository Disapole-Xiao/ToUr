from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import default_storage
from django.db import models
from django.core.files.base import ContentFile

from src.compress import compress, decompress

def dest_map_path(instance, filename):
    ''' 游学地图片存储路径 '''
    # 生成文件名
    filename = f'{instance.name}.cprs'
    path = 'dest_maps/' + filename
    # 检查文件是否存在并删除
    if default_storage.exists(path):
        default_storage.delete(path)
    return path


class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
    def __hash__(self) -> int:
        return hash(self.name)

class Destination(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=1, choices={('s', '景区'), ('u','学校')}, default='s')
    province = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    popularity = models.IntegerField(default=0, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True, validators=[
            # 限制0~5
            MinValueValidator(0, message="Rating must be at least 0"),
            MaxValueValidator(5, message="Rating cannot be greater than 5"),
        ])
    tags = models.ManyToManyField(Category)
    map = models.FileField(upload_to=dest_map_path, blank=True, null=True)

    def set_map(self, map: str):
        #确保文件以utf-8编码保存（否则会按照系统使用gb2312）
        map_bytes = map.encode('utf-8')
        self.map.save(self.map.name, ContentFile(map_bytes))
    def get_map(self) -> str:
        with self.map.open('rb') as f:
            byte_stream = f.read()
        return decompress(byte_stream)
    def __str__(self):
        return self.name
    def __hash__(self) -> int:
        return hash(self.name)
    def save(self, *args, **kwargs):
        # 是否上传了该字段
        if self.map:
            # 原map大小
            old_map_size= self.map.size
        
            # 读取map文件内容为字符串，调用 compress 函数压缩上传的文件
            with open(self.map.path, 'r', encoding='utf-8') as f:
                string = f.read()
            compressed_content = compress(string)
        
            # 保存压缩后的内容到 map 字段
            self.map.save(self.map.name, ContentFile(compressed_content), save=False)
            print('-----原文件大小', old_map_size, 'bytes')
            print('-----压缩后大小', self.map.size, 'bytes')
            print('-----压缩比', old_map_size / self.map.size)
            
        super(Destination, self).save(*args, **kwargs)
    
class AmenityType(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
    def __hash__(self) -> int:
        return hash(self.name)
    
class RestaurantType(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
    def __hash__(self) -> int:
        return hash(self.name)
