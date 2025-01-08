import requests
import parsel
import csv

for page in range(1,101):
    print(f'正在爬取第 {page} 页...')
    # 设置目标URL和请求头
    url = f"https://nj.lianjia.com/ershoufang/pg{page}/"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Cookie": "mediav=%7B%22eid%22%3A%22202234%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22%24ysJwn%5ExQy9d17%5B%3AsM9C%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22%24ysJwn%5ExQy9d17%5B%3AsM9C%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; lianjia_uuid=c102ef0a-438b-456b-9231-1b2949ad2fc3; _jzqckmp=1; sajssdk_2015_cross_new_user=1; _ga=GA1.2.559104077.1732495366; _gid=GA1.2.2102186829.1732495366; select_city=320100; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219360c52401ae6-0a1eff8fae51c3-4c657b58-1327104-19360c524021c9d%22%2C%22%24device_id%22%3A%2219360c52401ae6-0a1eff8fae51c3-4c657b58-1327104-19360c524021c9d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga_BP33PMLH1S=GS1.2.1732495600.1.0.1732495600.0.0.0; crosSdkDT2019DeviceId=j5hv1e-8pbec2-nt2lpap7ey6sqhb-h8lzkxvyp; lianjia_ssid=c37ab25e-d379-4bf9-b20a-4e6d47a2e041; login_ucid=2000000456238892; lianjia_token=2.00154ef51042e63fd004e3dc21f0108d36; lianjia_token_secure=2.00154ef51042e63fd004e3dc21f0108d36; security_ticket=ANZTE/orcRttZwmHYjV8IrFsyiZAcc/Nv3TrnCbTl0WAd0R84+KuWtw8pKcRktr+kA1EECZUPxELzRSoycid8ZMlIVO3Hds8s21bPkvMLn1q8L6FWqVmdjT9UrqZ9rcIt6eVzDaJj4IZaA4Mk1hReesBMCp2RyItky/ua04W0IE=; ftkrc_=9f85fd7c-6d3f-4fc6-89c0-779cf355c0b5; lfrc_=390f9069-8cb5-4c5c-be28-68e19e41350c; _qzjc=1; _jzqc=1; _jzqx=1.1732495353.1732542557.2.jzqsr=link%2Ezhihu%2Ecom|jzqct=/.jzqsr=clogin%2Elianjia%2Ecom|jzqct=/; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1732495353,1732542557; HMACCOUNT=111F056737FC8704; Qs_lvt_200116=1732495626%2C1732542556; _jzqa=1.2216552852153332200.1732495353.1732542557.1732548252.3; Qs_pv_200116=1695954293727528200%2C2280143077051374600%2C2722878572836210700%2C4522670897113890300%2C3114174840921158700; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1732549572; _qzja=1.372583657.1732495408563.1732542556599.1732548252019.1732548252019.1732549572001.0.0.0.13.3; _qzjb=1.1732548252019.2.0.0.0; _qzjto=13.3.0; _jzqb=1.2.10.1732548252.1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYTVmYTdlMGQxMjBkMjBiZTllYmE1NTRiZGU4MTYwMmFjYTQwNDEwYjFlMjkwODgyOWUyZWMxYjE0NTM4NmYxOWRkMDlkM2I5OWY2NmUyNDVkMDg4ZTRiNjJkY2RjMTg5ZWYyMjVkMjEyMzI4NGM0MmVlYjZiYmMzZDIyYmM4NDMxZmFlNzIxZDQwMzAwN2ZmMTY2NTg4ZDhhODdjMDk5ZmE3NTc5ZjBiNDc5YmM0MWM4NzdkZTU4OWZlY2RkMDY2NzQyZjlmNmViN2YxY2ZhMWY0YjI0NjgzYmE0ZTdiYzFmMmQ5MjY3NDkyNzhmMzA4NmFjYmIxNDAxZWQzZjdlY1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI5NmYzNjUzZlwifSIsInIiOiJodHRwczovL25qLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; _ga_E91JCCJY3Z=GS1.2.1732548264.3.1.1732549584.0.0.0; _ga_MFYNHLJT0H=GS1.2.1732548264.3.1.1732549584.0.0.0"
    }

    # 获取网页HTML内容
    response = requests.get(url=url, headers=headers)
    html_data = response.text
    selector = parsel.Selector(html_data)


    # 提取房源信息
    lis = selector.css('li.clear.LOGVIEWDATA.LOGCLICKDATA')  # 定位到每个房源

    for li in lis:
        # 提取标题
        title = li.css('.title a::text').get()
        # 提取小区名
        addressinfo = li.css('.flood .positionInfo a::text').get()
        # 提取房屋详情
        sizeinfo = li.css('.houseInfo::text').get()
        # 提取关注人数和发布时间
        followinfo = li.css('.followInfo::text').get()
        # 提取总价和单价
        total_price = li.css('.totalPrice span::text').get() + "万"
        unit_price = li.css('.unitPrice span::text').get()
        with open('NanJingHousing.csv',mode='a',encoding='utf-8',newline='')as f:
             csv_writer=csv.writer(f)
             csv_writer.writerow([title,addressinfo,sizeinfo,followinfo,total_price,unit_price])
    