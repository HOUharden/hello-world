import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# 创建一个地理编码器对象
geolocator = Nominatim(user_agent="1774259320@qq.com")

def get_lat_lon(location, retries=1):
    try:
        loc = geolocator.geocode(location, timeout=5)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        if retries > 0:
            time.sleep(2)  # 等待2秒后重试
            return get_lat_lon(location, retries - 1)
        else:
            print(f"Service timed out for {location}")
            return None, None
    except Exception as e:
        print(f"Error getting location for {location}: {e}")
        return None, None

# 读取Excel表格
df = pd.read_excel(r'C:\Users\86156\Desktop\area2.xlsx')

# 打印列名以确认实际的列名
print("列名：", df.columns)

# 假设地区名在实际的列名中，比如“地区名”或其他合适的名字
location_column = 'location'  # 替换为实际的列名

df['latitude'] = None
df['longitude'] = None

for idx, row in df.iterrows():
    lat, lon = get_lat_lon(row[location_column])
    df.at[idx, 'latitude'] = lat
    df.at[idx, 'longitude'] = lon
    print(f"Processed {row[location_column]}: {lat}, {lon}")
    time.sleep(1)  # 加入延迟以避免被API限制

# 将结果保存回Excel
df.to_excel(r'C:\Users\86156\Desktop\locations_with_coordinates.xlsx', index=False)
