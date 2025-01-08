import csv
import pandas as pd
import numpy as np

pi = 3.1415926
House_Price = []
with open('NanJingHousing—v2.csv', encoding='utf-8') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        unit_price = row['单价'].replace('元/平', '').replace(',', '')
        info = {
            '经度': float(row['经度']),
            '纬度': float(row['纬度']),
            '单价': float(unit_price)
        }
        House_Price.append(info)

Train_info = []
with open('NanJingHousingwithsubway.csv', encoding='utf-8') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        info = {'address': row['address'],
                '经度': float(row['经度']),
                '纬度': float(row['纬度']),
                'Serise_X': float(row['Serise_X']),
                'Serise_Y': float(row['Serise_Y'])}
        Train_info.append(info)

N_House = len(House_Price)
N_Train = len(Train_info)
Thresold_D = 2  # 单位应该是千米

# 修改此处，使用DataFrame来存储Train_info和计算出的平均价格
train_df = pd.DataFrame(Train_info)

for i in range(N_Train):
    Stat_x = train_df.loc[i, '经度']
    Stat_y = train_df.loc[i, '纬度']
    Neighbor = []
    for j in range(N_House):
        House_x = House_Price[j]['经度']
        House_y = House_Price[j]['纬度']
        # 计算两点之间的距离
        D = np.arccos(np.sin(Stat_x * pi / 180) * np.sin(House_x * pi / 180) +
                      np.cos(Stat_x * pi / 180) * np.cos(House_x * pi / 180) * np.cos(Stat_y * pi / 180 - House_y * pi / 180)) * 6371.004
        if D <= Thresold_D:
            Neighbor.append(House_Price[j]['单价'])
    # 计算平均价格，并处理空列表的情况
    mean_price = np.mean(Neighbor) if Neighbor else np.nan
    # 将平均价格添加到DataFrame
    train_df.loc[i, '平均价格'] = mean_price

# 将修改后的DataFrame保存到CSV文件
train_df.to_csv('NanJingHousingwithsubway_updated.csv', index=False, encoding='utf-8')
