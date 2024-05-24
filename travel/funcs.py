import math
def compute_interest_match(dest, user) -> int:
    ''' 返回游学地与用户的兴趣匹配度 '''
    tags = dest.tags.all()
    interests = user.interests.all()
    match_count = sum(category in tags for category in interests)
    return match_count


def distance(lat1, lon1, lat2, lon2):
    EARTH_RADIUS = 6371  # 地球平均半径，单位为公里
    rad_lat1 = math.radians(lat1)
    rad_lat2 = math.radians(lat2)
    a = rad_lat1 - rad_lat2
    b = math.radians(lon1) - math.radians(lon2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                 math.cos(rad_lat1) * math.cos(rad_lat2) * math.pow(math.sin(b / 2), 2)))
    s = s * EARTH_RADIUS * 1000 # 单位米
    s = round(s, 1)  # 保留1位小数
    return s

if __name__ == '__main__':
    print(distance(39.937873, 116.33387, 39.937849, 116.333392))
    