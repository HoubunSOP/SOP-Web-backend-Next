from meilisearch import Client

meili_client = Client('http://192.168.232.131:7700', 'KORQifkDLo4VyOI1QoSo4yA2Cl0UHvkNLxdfP0EIJwc')

async  def create_index():
    meili_client.create_index('comics',{'primaryKey': 'id'})
    meili_client.create_index('magazines',{'primaryKey': 'id'})
    meili_client.create_index('articles',{'primaryKey': 'id'})

async def init_indices():
    await create_index()
    comics_index = meili_client.index('comics')
    comics_index.update_settings({
        'searchableAttributes': ['name', 'original_name', 'intro'],
        'filterableAttributes': ['author_id', 'date', 'category_ids', 'isbn'],
    })

    magazines_index = meili_client.index('magazines')
    magazines_index.update_settings({
        'searchableAttributes': ['name', 'intro'],
        'filterableAttributes': ['publish_date', 'category_ids', 'id']
    })

    articles_index = meili_client.index('articles')
    articles_index.update_settings({
        'searchableAttributes': ['title', 'content', 'comic'],
        'filterableAttributes': ['date', 'recommended', 'category_ids', 'author_id']
    })