from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import csv

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument("window-size=1920x1080")
options.add_argument(f"user-agent={user_agent}")
browser = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
# 크롬 업데이트로 install 필요 pip install --upgrade webdriver_manager

# 쿼리분석 도쿄
# https://wing.hanatour.com/package/major-products?
# cntryCd=JP&
# cityCd=TYO&
# depCityCd=JCN%2CAF9&
# pkgServiceCd=FP&
# flag=ICE&
# rprsProdAirEnn=Y%2CN&
# prodTypeCd=G%2CI&
# strtDepDay=20231001&
# endDepDay=20231031&
# depCityNm=%EC%9D%B8%EC%B2%9C%2F%EA%B9%80%ED%8F%AC

# %2는 콤마
# https://wing.hanatour.com/package/major-products?
# cntryCd=JP&
# cityCd=OSA&
# depCityCd=JCN%2CAF9&
# pkgServiceCd=FP&
# flag=ICE&
# rprsProdAirEnn=Y%2CN&
# prodTypeCd=G%2CI&
# strtDepDay=20231001&
# endDepDay=20231031&
# depCityNm=%EC%9D%B8%EC%B2%9C%2F%EA%B9%80%ED%8F%AC

# 변경가능 코드
# strtDepDay= 출발일
# endDepDay= 도착일
# cntryCd= 국가
# cityCd= 도시
# depCityNm= 출발지역

strtDepDay = "20231001"
endDepDay = "20231031"
cntryCd = "JP"
cityCd = "TYO"

url = f"https://wing.hanatour.com/package/major-products?cntryCd={cntryCd}&"
url += f"cityCd={cityCd}&depCityCd=JCN%2CAF9&pkgServiceCd=FP&flag=ICE&rprsProdAirEnn=Y%2CN&prodTypeCd=G%2CI&"
url += f"strtDepDay={strtDepDay}&endDepDay={endDepDay}&depCityNm=%EC%9D%B8%EC%B2%9C%2F%EA%B9%80%ED%8F%AC"
all_hash_tags = []

browser.get(url)
soup = BeautifulSoup(browser.page_source, "html.parser")
items = soup.select("ul.type > li")
t_item = []
counter = 1

for i in items:
    img_nodes = i.select_one("div.inr.img>img")  # 확인
    # 리스트가 비어있지 않고 첫 번째 요소에 'src' 속성이 있는 경우
    if img_nodes and 'src' in img_nodes.attrs:
        img = img_nodes['src']
        print(img)
    else:
        img = "이미지 없음"
    cate_node = i.select_one("span.attr")  # none 있음
    if cate_node is not None:
        cate = cate_node.get_text().strip()
    else:
        cate = "카테고리 없음"
    title = i.select_one("strong.item_title.eps3").get_text().strip()  # 확인
    sub_t = i.select_one("p.item_text.stit").get_text().strip()  # 확인
    text_node = i.select_one("span.icn.cal")
    if text_node is not None:
        trip_term = text_node.contents[0].strip()
        # print(trip_term)

    hash_list = i.select("span.hash_group")
    for j in hash_list:
        hash_tags = j.select("span")
        # 리스트 컴프리헨션: 기존 리스트를 바탕으로 새로운 리스트를 생성
        group_hash = [tag.get_text().strip() for tag in hash_tags]
        all_hash_tags.append(group_hash)
    price_node = i.select_one("strong.price")
    if price_node is not None:
        price = price_node.contents[0].strip()
        # print(price)
        # 딕셔너리로 리스트 넣기
        item_dict = {
            'id': counter,
            'title': title,
            'price_pc': price,
            'link': url,
            'mobile_link': '없음',
            'image_link': img,
            'category_name1': cate,
            'Shipping': 0}

        t_item.append(item_dict)
        # print(item_dict)

        counter += 1

print(t_item)
file_name = "hana_jp_tyo.csv"
path = "./data_excel/"
with open(path+file_name, 'w', newline='',  encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=[
                            'id', 'title', 'price_pc', 'link', 'mobile_link', 'image_link', 'category_name1', 'Shipping'])
    writer.writeheader()  # 헤더 쓰기
    writer.writerows(t_item)  # 데이터 쓰기
    print("엑셀 파일 완성")

print("완성 파일 확인하세요 🥰")
