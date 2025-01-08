import pandas as pd
import requests
import json
import time

# 读取输入文件
df = pd.read_csv('NanJing_version1.csv', encoding='utf-8-sig')
df["经度"] = None
df["纬度"] = None

# 高德地图 API 配置
api_key = "db41c33475b37ab61d4eed062b415fdd"
base_url = "https://restapi.amap.com/v3/geocode/geo"

# 遍地铁名并获取经纬度信息
for i, addr in enumerate(df["name"]):
    try:
        # 为地址添加 "南京市" 前缀
        full_address = f"南京市{addr}（地铁站）"
        
        params = {
            "key": api_key,
            "address": full_address
        }
        
        # 发起 API 请求
        response = requests.get(base_url, params=params)
        result = response.json()
        
        # 打印响应信息，查看是否有 geocodes 返回
        print(f"处理地址：{full_address}")
        print("响应数据：", result)  # 打印响应数据

        if result.get("status") == "1" and result.get("geocodes"):
            geo_info = result["geocodes"][0]
            location = geo_info["location"].split(",")
            df.loc[i, "经度"] = location[0]
            df.loc[i, "纬度"] = location[1]
        else:
            print(f"未找到地址：{full_address}")
            df.loc[i, "经度"] = "N/A"
            df.loc[i, "纬度"] = "N/A"
    except Exception as e:
        print(f"处理地址 {full_address} 时出错：{e}")
        df.loc[i, "经度"] = "N/A"
        df.loc[i, "纬度"] = "N/A"

    # 避免 API 调用频率过高，设置更长的延时（比如1秒）
    time.sleep(1)

# 保存结果到原文件
output_file = 'NanJing_version1_with_coordinates.csv'  # 保存为新文件
df.to_csv(output_file, index=False, encoding="utf-8-sig")
