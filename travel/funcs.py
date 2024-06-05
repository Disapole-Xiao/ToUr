import math
def compute_interest_match(dest, user) -> int:
    ''' 返回游学地与用户的兴趣匹配度 '''
    tags = dest.tags.all()
    interests = user.interests.all()
    match_count = sum(category in tags for category in interests)
    return match_count

def comprehensive_tuple(dest, user):
    ''' 返回游学地的综合权重 '''
    interest_match = compute_interest_match(dest, user)
    return (interest_match, dest.rating, dest.popularity)

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

def make_route_key(attr_ids, mode, allow_ride):
    if len(attr_ids) <= 1:
        return None
    if len(attr_ids) == 2:
        return f'{attr_ids[0]}_{attr_ids[1]}_{mode}_{allow_ride}'
    start = attr_ids[0]
    seq = [str(i) for i in sorted(attr_ids[1:])]
    return f"{start}_{'_'.join(seq)}_{mode}_{allow_ride}"


if __name__ == '__main__':
    print(make_route_key([-1,4,2,6,5], 'distance',True))
    print(make_route_key([-1,4], 'time', False))
    