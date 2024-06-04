'''
自动存储对象到数据库
'''
import json, os, random, sys

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
from diary.models import *
from account.models import *

# 以下写你的代码

def fill_amenity_type():
    ''' 设施类型 '''
    li = ["卫生间","喷泉","公共电话亭","外卖柜","快递站","商店","医务室","观景台","眼镜店","打印店"]
    for i in li:
        AmenityType.objects.create(name=i)
    print("amenity_type filled")

def fill_restaurant_type():
    li = ['火锅', '烧烤', '甜品', '海鲜', '外国菜', '汤/粥/炖菜', '家常菜', '小吃快餐']
    for i in li:
        RestaurantType.objects.create(name=i)
    print("restaurant_type filled")  

def set_dest_map(dest: Destination, map_id: int):
    with open(f"static/maps/{map_id}.json", "r", encoding='utf-8') as f:
        map_dict = json.load(f)
    map_dict['name'] = dest.name
    s = json.dumps(map_dict, ensure_ascii=False)
    dest.set_map(s)
    print(f"dest_map of {dest.name} filled with {map_id}")
def fill_dest_map():
    for dest in Destination.objects.all():
        # 如果是景区
        if dest.type == "s":
            map_id = random.choice([1,4])
        # 如果是学校
        elif dest.type == "u":
            map_id = random.choice([2,3])
        set_dest_map(dest, map_id)
    print("dest_map filled")

if __name__ == "__main__":
    # fill_dest_map()
    # set_dest_map(Destination.objects.get(name="北京动物园"), 1)
    # set_dest_map(Destination.objects.get(name="北京大学"), 2)
    # set_dest_map(Destination.objects.get(name="清华大学"), 3)
    # set_dest_map(Destination.objects.get(name="故宫博物院"), 4)
    for diary in Diary.objects.all():
        diary.save()