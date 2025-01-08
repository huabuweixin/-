import requests
import json
import csv
from DrissionPage import ChromiumPage
from time import sleep
from DrissionPage.errors import ElementLostError

dp = ChromiumPage()
f = open('hoteldata.csv', mode='a', encoding='utf-8-sig', newline='')  # 避免空白行
csv_writer = csv.DictWriter(f, fieldnames=[
    '酒店',
    '评论',
    '价格',
    '地址',
    '纬度',
    '经度',
])
csv_writer.writeheader()

# 记录已插入的酒店名称，避免重复
inserted_hotels = set()

dp.listen.start('json/HotelSearch')
dp.get('https://hotels.ctrip.com/hotels/list?countryId=1&city=12&provinceId=0&checkin=2024/12/08&checkout=2024/12/09&optionId=12&optionType=City&directSearch=0&display=%E5%8D%97%E4%BA%AC&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&')

for page in range(1, 100):
    print(f'正在采集第{page}页数据')
    dp.scroll.to_bottom()  # 滚动到底部，确保加载了所有数据

    if page > 2:
        try:
            next_page = dp.ele('css:.btn-box span')
            if next_page and next_page.text == '搜索更多酒店':
                sleep(2)  # 等待页面加载稳定
                next_page = dp.ele('css:.btn-box span')  # 再次获取最新的元素
                next_page.click()
        except ElementLostError:
            print("元素失效，重新定位中...")
            dp.scroll.to_bottom()
            next_page = dp.ele('css:.btn-box span')
            if next_page and next_page.text == '搜索更多酒店':
                next_page.click()
    
    resp = dp.listen.wait()  # 等待响应
    if resp and resp.response and resp.response.body:
        json_data = resp.response.body
        if isinstance(json_data, dict) and 'Response' in json_data:
            hotel_list = json_data.get('Response', {}).get('hotelList', {}).get('list')
            if hotel_list is not None:
                for index in hotel_list:
                    # 提取数据
                    hotel_name = index.get('base', {}).get('hotelName', '').strip()
                    comment = index.get('comment', {}).get('content', '').strip()
                    price = index.get('money', {}).get('price', '').strip()
                    address = index.get('position', {}).get('address', '').strip()
                    lat = index.get('position', {}).get('lat', '')
                    lng = index.get('position', {}).get('lng', '')

                    # 检查酒店名称是否为空或已插入
                    if not hotel_name or hotel_name in inserted_hotels:
                        continue
                    
                    # 创建数据字典
                    dit = {
                        '酒店': hotel_name,
                        '评论': comment,
                        '价格': price,
                        '地址': address,
                        '纬度': lat,
                        '经度': lng,
                    }

                    # 写入数据并记录已插入酒店
                    csv_writer.writerow(dit)
                    inserted_hotels.add(hotel_name)  # 记录酒店名称
