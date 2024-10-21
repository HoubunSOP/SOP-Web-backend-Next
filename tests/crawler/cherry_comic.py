import requests
from bs4 import BeautifulSoup


def extract_comic_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # 获取漫画简介
    comic_detail = soup.find(id='comic_detail').find('p')
    for br in comic_detail.find_all('br'):
        br.decompose()
    comic_description = comic_detail.contents[0]

    # 信息栏中的相关信息
    detail_table = soup.find("div", class_="detail_table")
    extracted_data = {}
    if detail_table:
        table = detail_table.find("table")
        rows = table.find_all("tr")

        target_fields = ["タイトル", "著者", "レーベル", "巻", "ISBN"]

        for row in rows:
            th = row.find("th")
            td = row.find("td")

            if th and td:
                field_title = th.text.strip()
                if field_title in target_fields:
                    extracted_data[field_title] = td.text.strip()

    # 书影图片URL
    comic_detail = soup.find(id="comic_detail")
    img_src = None
    if comic_detail:
        img = comic_detail.find("img")
        if img:
            img_src = img["src"]

    detail_table = soup.find("table", id="status_table")

    # 找到标有"詳細"的行
    row = None
    for tr in detail_table.find_all('tr'):
        if tr.th is not None and '詳細' in tr.th.text:
            row = tr
            break

    # 从找到的行中提取URL
    kirara_src = None
    if row is not None:
        url_cell = row.find('td', class_='status_data')
        if url_cell is not None:
            kirara_src = url_cell.find('a')['href']
    # 找到标有"書影"的行
    row = None
    for tr in detail_table.find_all('tr'):
        if tr.th is not None and '書影' in tr.th.text:
            row = tr
            break

    # 从找到的行中提取URL
    img_kirara_src = None
    if row is not None:
        url_cell = row.find('td', class_='status_data')
        if url_cell is not None:
            img_kirara_src = url_cell.find('a')['href']

    return comic_description, extracted_data, img_src, img_kirara_src, kirara_src


url = "http://192.168.33.128:3000/comics_detail/1944.html"  # 将此 URL 替换为您要提取内容的网页 URL
comic_description, extracted_data, img_src, img_kirara_src, kirara_src = extract_comic_info(url)

print("Comic Description:", comic_description)
print("Extracted Data:", extracted_data)
print("Image Source URL:", img_src)
print("Image Kirara Source URL:", img_kirara_src)
print("Kirara URL:", kirara_src)
