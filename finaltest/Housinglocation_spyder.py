import pandas as pd
import requests
import json
import time

# 读取输入文件
df = pd.read_csv('NanJingHousing.csv', encoding='utf-8-sig')

# 添加用于存储结果的新列
df["经度"] = None
df["纬度"] = None
df["格式化地址"] = None
df["地址级别"] = None

# 高德地图 API 配置
api_key = "5315c0d4d666bfdb0cdb905ff78fea98"
base_url = "https://restapi.amap.com/v3/geocode/geo"

# 遍历小区名并获取经纬度信息
for i, addr in enumerate(df["小区名"]):
    try:
        # 为地址添加 "南京市" 前缀
        full_address = f"南京市{addr}"
        
        params = {
            "key": api_key,
            "address": full_address
        }
        response = requests.get(base_url, params=params)
        result = response.json()

        if result.get("geocodes"):
            geo_info = result["geocodes"][0]
            location = geo_info["location"].split(",")
            df.loc[i, "经度"] = location[0]
            df.loc[i, "纬度"] = location[1]
            df.loc[i, "格式化地址"] = geo_info["formatted_address"]
            df.loc[i, "地址级别"] = geo_info["level"]
        else:
            print(f"未找到地址：{full_address}")
    except Exception as e:
        print(f"处理地址 {full_address} 时出错：{e}")

    # 避免 API 调用频率过高
    time.sleep(0.1)

# 保存结果到原文件
output_file = 'NanJingHousing.csv'  # 可更改路径以保存为新文件
df.to_csv(output_file, index=False, encoding="utf-8-sig")
print("地理编码任务完成并保存至文件。")
