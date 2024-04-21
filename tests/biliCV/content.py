import asyncio
import json

from bilibili_api import article, sync
from bs4 import BeautifulSoup


async def main():
    # 创建专栏类
    ar = article.Article(29100479)
    # 如果专栏为公开笔记，则转换为笔记类
    # NOTE: 笔记类的函数与专栏类的函数基本一致
    if ar.is_note():
        ar = ar.turn_to_note()
        print("qwq")
    # 加载内容
    resp = await ar.get_all()
    document = BeautifulSoup(f"<div>{resp['readInfo']['content']}</div>", "lxml")

    # 将 data-src 更改为 src
    for img in document.select('img[data-src]'):
        img['src'] = img['data-src']
        del img['data-src']

    # 写入 markdown
    with open('article.temp.html', 'w', encoding='utf8') as f:
        f.write(str(document))


if __name__ == "__main__":
    asyncio.run(main())