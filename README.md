# In Development

A Telegram bot that helps track prices for products from various online stores (Amazon, Aliexpress, eBay, Wildberries).  
The bot is written in Python and uses the `aiogram` library to interact with the Telegram API.  
The project also includes asynchronous database operations using `SQLAlchemy` and `aiohttp` for making HTTP requests.

# Plans:
- Refactor the project to a microservice architecture.
- Replace SQLite (used as a test database) with PostgreSQL.
- Add queues for price updates using `Celery` and `Redis`.
- Implement the ability to generate price trend graphs.

## Dependencies:
- Python 3.11.0
- aiogram 3.3.0
- python-dotenv 1.0.0
- BeautifulSoup 0.0.2
- requests 2.32.3
- lxml 5.3.0
- SQLAlchemy 2.0.25
- asyncpg 0.29.0
- aiosqlite 0.19.0
- apscheduler 3.11.0
