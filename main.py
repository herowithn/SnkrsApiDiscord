import requests, json, pickle, time, discord
from discord import Webhook, SyncWebhook
import aiohttp
products = []
class Product():
    def __init__(self, title, color, portrait, sku, price, drop_date, method):
        self.title = title + ' ' + color
        self.portrait = portrait
        self.sku = sku
        self.price = str(price) + 'PLN'
        self.drop_date = drop_date[:-14]
        self.method = method
def find_product(search_id):
    for product in products:
        if product.sku == search_id:
            return product
    return None
def send_webook(embed):
    webhook = SyncWebhook.from_url(YOUR_WEBHOOK)
    webhook.send(embed=embed)
def request_products():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    store_api = 'https://api.nike.com/product_feed/threads/v3/?anchor=0&count=50&filter=marketplace%28PL%29&filter=language%28pl%29&filter=upcoming%28true%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29&sort=effectiveStartSellDateAsc'
    req = requests.get(store_api, headers=headers)
    if req.status_code != 200:
        print(f"Request failed: {req.status_code}")
        return
    json_dict = json.loads(req.text)
    for i in range(0, len(json_dict['objects'])):
        title = json_dict['objects'][i]['publishedContent']['properties']['coverCard']['properties']['subtitle']
        color = json_dict['objects'][i]['publishedContent']['properties']['coverCard']['properties']['title']
        portrait = json_dict['objects'][i]['publishedContent']['properties']['coverCard']['properties']['portraitURL']
        sku = json_dict['objects'][i]['id']
        price = json_dict['objects'][i]["productInfo"][0]['merchPrice']['currentPrice']
        drop_date = json_dict['objects'][i]['productInfo'][0]['launchView']['startEntryDate']
        method = json_dict['objects'][i]['productInfo'][0]['launchView']['method']
        x = Product(title,color,portrait,sku,price, drop_date, method)
        print(str(sku)+'\n')
        if find_product(x.sku) != None:
            print("Ignoring product")
            continue
        else:
            products.append(x)
            embed = discord.Embed(title=x.title, color=0x00eeff)
            embed.set_author(name='New Drop')
            embed.set_image(
                url=x.portrait)
            embed.add_field(name="price:", value=str(x.price), inline=1)
            embed.add_field(name="drop date:", value=str(x.drop_date), inline=1)
            embed.add_field(name="drop method:", value=str(x.method), inline=1)
            print('1')
            send_webook(embed)
request_products()
