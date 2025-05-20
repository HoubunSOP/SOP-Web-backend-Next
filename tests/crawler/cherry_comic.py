# 简易爬虫，填充示例数据

import re
from datetime import datetime, date
from xml.etree import ElementTree as ET

import pytz
import requests
from bs4 import BeautifulSoup
from fastapi import Depends
from sqlalchemy.orm import Session

from utils.database import get_db
from models.category import Category
from models.comic import ComicAuthor, Comic
from models.magazine import magazine_category_map, magazine_comic_map, Magazine
from schemas.comic import AutoComicCreate
from schemas.magazine import MagazineCreate


# 为了能够获取到5月30的书而实现12月30的日期效果
def add_months(date_obj):
    month = date_obj.month - 1 + 7  # 减1是因为月份是从0开始的
    year = date_obj.year + month // 12  # 整除得到年份的增加
    month = month % 12 + 1  # 取余得到新的月份，加1是因为月份是从1开始的
    day = min(date_obj.day,
              [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31,
               30, 31][month - 1])  # 考虑闰年和每个月的天数
    return date(year, month, day)


def extract_comic_info(url):
    response = requests.get('https://krr.cherry-takuan.org/comics_detail/?cid=' + url)
    soup = BeautifulSoup(response.content, "html.parser")

    # 获取漫画简介
    comic_detail = soup.find(id='comic_detail').find('p')
    for br in comic_detail.find_all('br'):
        br.decompose()
    comic_description = "\n".join(comic_detail.contents).replace("\n\t\t\t\t\t", "")

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
    if not extracted_data['タイトル'] or not extracted_data['巻']:
        target_href = "https://www.example.com"
        first_a_tag = soup.find('a', href=target_href)
        text_of_first_a_tag = first_a_tag.text
        # 使用正则表达式匹配文字和数字
        match = re.match(r'(.+) - (\d+)', text_of_first_a_tag)

        if match:
            # 提取匹配到的组
            name = match.group(1)  # 文字部分
            volume = match.group(2)  # 数字部分
    else:
        name = extracted_data['タイトル']
        volume = extracted_data['巻']

    api_url = "https://ndlsearch.ndl.go.jp/api/opensearch?isbn=" + extracted_data['ISBN']

    # 发送请求获取RSS数据
    response = requests.get(api_url)
    rss_data = response.content
    # 解析RSS XML数据
    root = ET.fromstring(rss_data)

    # 提取pubDate字段
    pub_date_str = root.find(".//pubDate").text

    # 转换时区
    # 假设pubDate是UTC时间
    utc_pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
    # 转换为+8时区
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_pub_date = utc_pub_date.astimezone(beijing_tz)

    # 将日期转换为date类型
    beijing_pub_date = add_months(beijing_pub_date.date())
    comic_data = AutoComicCreate(
        name=name,
        original_name=name,
        date=beijing_pub_date,
        intro=comic_description,
        cover=img_kirara_src,
        isbn=extracted_data['ISBN'],
        cid=url,
        volume=volume,
        author_name=extracted_data['著者']
    )

    return comic_data


def add_comicdb(comic: AutoComicCreate, db: Session = Depends(get_db)):
    # 默认爬取的漫画分类为其他
    category_id = 5
    try:
        # 检查分类是否存在
        category = db.query(Category).filter(Category.id == category_id).first()
        # 查找或创建作者
        author = db.query(ComicAuthor).filter(ComicAuthor.name == comic.author_name).first()
        if not author:
            author = ComicAuthor(name=comic.author_name)
            db.add(author)
            db.commit()
            db.refresh(author)

        # 创建漫画实例
        new_comic = Comic(
            name=comic.name,
            original_name=comic.original_name,
            author_id=author.id,
            date=comic.date,
            intro=comic.intro,
            cover=comic.cover,
            auto=True,
            isbn=comic.isbn,
            cid=int(comic.cid),
            volume=comic.volume
        )

        # 关联分类
        new_comic.categories.append(category)

        # 保存到数据库
        db.add(new_comic)
        db.commit()
        db.refresh(new_comic)
        print("添加完成：" + str(comic.cid))
    except Exception as e:
        print("添加失败：" + str(comic.cid) + "原因：" + str(e))
        exit()
    return


def add_magazine(magazine_data: MagazineCreate, db: Session = Depends(get_db)):
    """
    创建新的杂志，并关联漫画和分类。
    :param magazine_data: 包含杂志信息及漫画名称列表
    """
    try:
        # 获取或创建默认分类（如果没有指定分类）
        category_id = magazine_data.category_id if magazine_data.category_id else 5
        category = db.query(Category).filter(Category.id == category_id).first()

        # 创建新杂志
        new_magazine = Magazine(
            name=magazine_data.name,
            cover=magazine_data.cover,
            publish_date=magazine_data.publish_date,
            intro=magazine_data.intro,
            link=magazine_data.link
        )
        db.add(new_magazine)
        db.commit()
        db.refresh(new_magazine)

        # 关联分类
        magazine_category = magazine_category_map.insert().values(
            magazine_id=new_magazine.id,
            category_id=category.id
        )
        db.execute(magazine_category)

        # 处理漫画名称列表
        for comic_name in magazine_data.comics:
            # 如果漫画名称不存在，新增
            existing_comic = db.query(magazine_comic_map).filter(
                magazine_comic_map.c.magazine_id == new_magazine.id,
                magazine_comic_map.c.comic_name == comic_name
            ).first()
            if not existing_comic:
                new_comic = magazine_comic_map.insert().values(
                    magazine_id=new_magazine.id,
                    comic_name=comic_name
                )
                db.execute(new_comic)

        db.commit()
        print("添加完成：" + str(magazine_data.link))
    except Exception as e:
        print("添加失败：" + str(magazine_data.link) + "原因：" + str(e))
        exit()


# https://ndlsearch.ndl.go.jp/api/opensearch?isbn=9784832295148&dpid=iss-ndl-opac%20ma-db
# http://www.dokidokivisual.com/comics/past/

def to_comic(db):
    for url in range(1930, 1966):
        comic_data = extract_comic_info(str(url))
        add_comicdb(comic_data, db)
    return 'ok'


def extract_mz_info(url):
    response = requests.get('https://krr.cherry-takuan.org/magazine_detail/?mid=' + str(url))
    soup = BeautifulSoup(response.content, "html.parser")

    comic_detail = soup.find(id='magazine_detail')
    img = comic_detail.find("img")
    img_src = img["src"]
    comic_detail = comic_detail.find('p')
    for br in comic_detail.find_all('br'):
        br.decompose()
    comic_description = "\n\n".join(str(content) for content in comic_detail.contents).replace("<strong>",
                                                                                               "**").replace(
        "</strong>", "**")

    comic_description = comic_description
    # 找到所有的行
    rows = soup.find("div", class_="detail_table").find_all('tr')

    # 初始化一个空列表来存储结果
    titles = []

    # 遍历每一行
    for row in rows:
        # 在每一行中找到m_detail_title列
        m_detail_title_column = row.find('td', class_='m_detail_title')
        # 如果找到了a标签，则提取其文本并添加到列表中
        if m_detail_title_column and m_detail_title_column.a and m_detail_title_column.a.text:
            titles.append(m_detail_title_column.a.text)
    title = soup.find('title').text
    match = title.split("-")
    # 提取匹配到的组
    title = match[0].replace('\n', '')  # 文字部分
    mdate = match[1]  # 数字部分

    match = mdate.split("/")
    mmu = match[0] + '年' + match[1] + '月号'
    pdate = datetime.strptime(mdate, "%Y/%m")
    link = 'http://www.dokidokivisual.com/magazine/carat/book/index.php?mid=' + str(url)

    if title == 'まんがタイムきらら':
        category_id = 7
    elif title == 'まんがタイムきららMAX':
        category_id = 8
    elif title == 'まんがタイムきららキャラット':
        category_id = 9
    elif title == 'まんがタイムきららフォワード':
        category_id = 10
    else:
        category_id = 11
    title = title + ' ' + mmu
    data = MagazineCreate(
        name=title,
        publish_date=pdate,
        cover=img_src,
        intro=comic_description,
        link=link,
        comics=titles,
        category_id=category_id
    )
    return data


def to_mz(db):
    for qwqid in range(866, 993):
        add_magazine(extract_mz_info(qwqid), db)