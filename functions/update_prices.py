import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from functions.product import Product
from database.models import TrackList
from database.engine import session_maker

async def update_product_price(session: AsyncSession, product: TrackList):
    """
    Асинхронная функция для обновления цены товара.
    Получает цену с помощью парсера и обновляет данные в базе.
    """
    # Создаем объект Product для парсинга
    product_instance = Product(user_id=product.user_id, tag=product.tag, link=product.src)
    
    # Получаем новую цену
    await product_instance.parser(product_instance.link)
    
    # Обновляем цену в словаре
    current_date = list(product_instance.price.keys())[-1]  # получаем актуальную дату
    new_price = product_instance.price[current_date]
    
    # Обновляем запись в базе данных
    product.price = new_price
    
    # Сохраняем обновленный товар в базе данных
    async with session.begin():
        session.add(product)
    print(f"Цена товара с тегом {product.tag} обновлена на {new_price}")

async def update_prices(session: AsyncSession):
    """
    Функция для обновления цен для всех товаров в базе данных.
    """
    # Получаем все товары из базы данных
    result = await session.execute(select(TrackList).filter(TrackList.price != None))
    products = result.scalars().all()

    # Для каждого товара обновляем цену
    for product in products:
        await update_product_price(session, product)

async def schedule_price_update():
    """
    Функция для запуска обновления цен раз в 24 часа.
    """
    while True:
        async with session_maker() as session:
            await update_prices(session)
        
        # Пауза в 24 часа
        await asyncio.sleep(20)  # 86400 секунд = 24 часа
