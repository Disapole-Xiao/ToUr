'''
自动存储对象到数据库
'''
import os
import sys

# 设置 Django 项目根目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# 设置 Django 项目的设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'ToUr.settings'

# 初始化 Django
import django
django.setup()

# 导入你的模型
from travel.models import *  

# 以下写你的代码

def fill_amenity_type():
    ''' 设施类型 '''
    li = ["卫生间","喷泉","公共电话亭","外卖柜","快递站","商店","医务室","观景台"]
    for i in li:
        AmenityType.objects.create(name=i)
    print("amenity_type filled")

def fill_restaurant_type():
    li = ['火锅', '烧烤', '甜品', '海鲜', '外国菜', '汤/粥/炖菜', '家常菜', '小吃快餐']
    for i in li:
        RestaurantType.objects.create(name=i)
    print("restaurant_type filled")  

if __name__ == "__main__":
    fill_restaurant_type()
    fill_amenity_type()
