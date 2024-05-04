import requests
from bs4 import BeautifulSoup

# url = "file:///D:/misaka10843/Downloads/krr/magazine_detail/903.html"  # 将此 URL 替换为您要提取内容的网页 URL
# response = requests.get(url)
file_path = "tests/crawler/sample/comic_1668.html"  # 将此路径替换为您要打开的本地文件路径

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()
soup = BeautifulSoup(content, "html.parser")
detail_table = soup.find("div", class_="detail_table")

if detail_table:
    table = detail_table.find("table")
    rows = table.find_all("tr")

    target_fields = ["タイトル", "著者", "レーベル", "巻", "ISBN"]
    extracted_data = {}

    for row in rows:
        th = row.find("th")
        td = row.find("td")

        if th and td:
            field_title = th.text.strip()
            if field_title in target_fields:
                extracted_data[field_title] = td.text.strip()

    print(extracted_data)
comic_detail = soup.find(id="comic_detail")

if comic_detail:
    img = comic_detail.find("img")
    if img:
        img_src = img["src"]
        print(img_src)
