from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# 创建 ChromeOptions 对象并设置 Chrome 的安装路径
chrome_options = Options()
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# 设置 Chrome WebDriver 的路径
chrome_driver_binary = "D:/chromedriver-win64/chromedriver.exe"

# 实例化 Chrome WebDriver，并传入 ChromeOptions 对象
driver = webdriver.Chrome(executable_path=chrome_driver_binary, options=chrome_options)

# 打开百度地图网站
driver.get("https://map.baidu.com/")

# 在搜索框中输入"北京大学"
search_box = driver.find_element_by_id("sole-input")
search_box.send_keys("北京大学")
search_box.send_keys(Keys.RETURN)

# 等待加载完成
time.sleep(5)

# 点击"更多"，显示更多的地点信息
more_button = driver.find_element_by_xpath("//div[contains(@class, 'search-more')]")
more_button.click()

# 获取所有景点和设施的名称、介绍和经纬度
places = driver.find_elements_by_xpath("//div[contains(@class, 'search-item')]")
for place in places:
    name = place.find_element_by_class_name("n-blue").text
    intro = place.find_element_by_class_name("n-grey-truncate").text
    lng_lat = place.find_element_by_class_name("n-gray").text
    print("名称:", name)
    print("介绍:", intro)
    print("经纬度:", lng_lat)
    print("-" * 50)

# 关闭浏览器
driver.quit()
