import asyncio

from bilibili_api import user, Credential

from schemas.external.bilibili import CVData

credential = Credential(sessdata="", bili_jct="")
my_user = user.User(uid=1585955812, credential=credential)


async def main():
    articles = await my_user.get_articles()
    data = CVData.parse_obj(articles)
    for article in data.articles:

        print(article.id)

if __name__ == "__main__":
    asyncio.run(main())