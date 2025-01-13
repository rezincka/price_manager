# note: make order imports

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

import asyncio
from datetime import datetime
import re
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import TrackList
from functions import parser

from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker


# Product bugs:
#   - user_id and tag can repete, that causes an error with remove product (bug with db);
#   - if link to catalog, parser will select first price, that found (bug with parser);
class Product:
    """
    Represents a product with attributes:
    - user_id: id of tg user.
    - tag: A category or tag for the product.
    - link: URL of the product.
    - price: Parsed price data (list of floats).
    """
    def __init__(self, user_id: int, tag: str, link: str = ''):
        self.user_id = user_id
        self.tag = tag
        self.link = link
        self.price = {}


    
    async def parser(self):
        
        domain = urlparse(self.link).netloc
        if domain.startswith('www.'):
            domain = domain[4:]

        current_date = datetime.now().date().strftime('%Y-%m-%d')  


        # if bool(re.match(r'https://www\.amazon\.(com|co\.(uk|ca)|de|fr|it|jp|es|in|au|br|mx)/[-\w/]+(?:\?[\w=&%-]*)?', domain)):
        if domain == "amazon.com":
            price = await parser.amazon(self.link)
            self.price.update(
                {current_date: (price)})
        elif bool(re.match(r'https://www\.ebay\.com/itm/\d+', domain)):
            price = await parser.ebay(self.link)
            self.price.update(
                {current_date: (price)})
        elif bool(re.match(r'https://www\.aliexpress\.com/item/\d+', domain)):
            price = await parser.aliexpress(self.link)
            self.price.update(
                {current_date: (price)})
        elif bool(re.match(r'https://www\.wildberries\.ru/catalog/\d+/detail\.aspx', domain)):
            price = await parser.wildberries(self.link)
            self.price.update(
                {current_date: (price)})

    


    async def add(self, session: AsyncSession):    
        # parse price
        await self.parser()
        # add record to database
        async with session.begin():
            data = TrackList(
                user_id=self.user_id,
                tag=self.tag,
                src=self.link,
                price= self.price,
                )
            session.add(data)



    async def update(self):
        ...
    #     async with async_session() as session:
    #         async with session.begin():
    #             result = await session.execute(Item.__table__.select())
    #             items = result.fetchall()
    #             return items  # Возвращает список объектов


    async def remove(self, session: AsyncSession):
        async with session.begin():
        
            result = await session.execute(select(TrackList).filter(
                TrackList.user_id == self.user_id,
                TrackList.tag == self.tag
                ))
            
            item = result.scalar_one_or_none()
        
            if item:
                await session.delete(item)
                await session.commit()


    async def get_price(self, session: AsyncSession,):
        result = await session.execute(
            select(TrackList.price).where(
                TrackList.tag == self.tag,
                TrackList.user_id == self.user_id
            )
        )
        return result.scalars().all()  
    

    @staticmethod
    async def show_all(session: AsyncSession, user_id: int):
        async with session.begin():
            result = await session.execute(
                select(TrackList.tag).filter(TrackList.user_id == user_id)
            )
            tags = result.scalars().all()
            return tags
    
