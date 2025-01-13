import aiohttp
from bs4 import BeautifulSoup
import asyncio


async def amazon(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            try:
                price = (soup.find('span', {"class": 'a-price-whole'}).text +
                         soup.find('span', {"class": "a-price-fraction"}).text)
                price = float(price.replace(',', '.'))
            except AttributeError:
                price = None
    
    return price



async def ebay(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            try:
                price = soup.find('span', {'class': 'x-price-primary'}).text.strip()
                price = float(price.replace('$', '').replace(',', '').strip())
            except AttributeError:
                price = None
    
    return price



async def aliexpress(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            try:
                price = soup.find('span', {'class': 'price-current'}).text.strip()
                price = float(price.replace('US $', '').replace(',', '').strip())
            except AttributeError:
                price = None
    
    return price



async def wildberries(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            try:
                price = soup.find('span', {'class': 'price-block__final-price'}).text.strip()
                price = float(price.replace('₽', '').replace(' ', '').strip())
            except AttributeError:
                price = None
    
    return price

# Основная асинхронная функция
async def main():
    link = 'https://pt.aliexpress.com/item/1005006861190021.html?spm=a2g0o.home.pcJustForYou.4.31c81c91SVPkuO&gps-id=pcJustForYou&scm=1007.13562.416251.0&scm_id=1007.13562.416251.0&scm-url=1007.13562.416251.0&pvid=360cb81e-3eb3-4ebb-b559-253120131710&_t=gps-id:pcJustForYou,scm-url:1007.13562.416251.0,pvid:360cb81e-3eb3-4ebb-b559-253120131710,tpp_buckets:668%232846%238109%231935&pdp_npi=4%40dis%21EUR%2140.77%2114.40%21%21%21301.55%21106.48%21%40211b6c1717347373002366989ee22f%2112000038542465794%21rec%21PT%214847322259%21ABXZ&utparam-url=scene%3ApcJustForYou%7Cquery_from%3A'
    p = await aliexpress(link)
    print(p)

# Запуск асинхронной программы
if __name__ == "__main__":
    asyncio.run(main())
