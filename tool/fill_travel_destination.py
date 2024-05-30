import os
import sys
import xlrd
import random

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
from travel.models import Destination, Category

def extract_province_and_city(value):
    ''' 从字符串中提取省份和城市 '''
    parts = value.split(" > ")
    if len(parts) >= 5:
        province = parts[3].strip()
        city = parts[4].strip()
        return province, city
    return None, None

def fill_travel_destinations_from_xls(file_path):
    ''' 从 xls 文件中填充 travel_destination 数据 '''
    # 打开 xls 文件
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)

    # 设置 travel_destination 的初始 id
    current_id = 10

    # 从第一行开始遍历数据，第一行可能是表头，所以跳过
    for row_index in range(1, sheet.nrows):
        # 从 xls 文件中读取数据
        name = sheet.cell_value(row_index, 1)  # 第三项
        location_value = sheet.cell_value(row_index, 3)  # 第五项
        description = sheet.cell_value(row_index, 16)  # 第18项
        popularity = random.randint(0, 10000)  # 生成随机整数
        rating = round(random.uniform(3, 5), 1)  # 生成随机一位小数
        image_url = sheet.cell_value(row_index, 7)  # 第九项

        # 提取省份和城市信息
        province, city = extract_province_and_city(location_value)
        # 如果 description、province、city 或 image_url 为空，跳过当前 travel_destination
        if not description or not province or not city or not image_url:
            print(f"Skipping travel destination '{name}' due to missing description, province, city, or image_url.")
            continue

        image_urls = image_url.split(";")
        if image_urls:
            image_url = image_urls[0].strip()

        # 创建 Destination 对象并手动设置 id 字段的值
        travel_destination = Destination(
            name=name,
            type='s',  # 假设类型为 's'
            province=province,
            city=city,
            description=description,
            popularity=popularity,
            rating=rating,
            image_url=image_url
        )

        # 保存 Destination 对象到数据库中
        travel_destination.save()

        nature_category = Category.objects.get(name="自然风光")
        travel_destination.tags.add(nature_category)

        print(f"Travel destination '{name}' added with ID {current_id}.")

        # 更新当前 id 的值
        current_id += 1

        # 如果填充了 100 项数据，结束循环
        if current_id > 120:
            break

    print("All travel destinations added.")

if __name__ == "__main__":
    # 传入 xls 文件的路径
    xls_file_path = "tool/spot.xls"
    fill_travel_destinations_from_xls(xls_file_path)
