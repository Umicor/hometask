import asyncio
import aiohttp
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///data.db", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ScrapedData(Base):
    __tablename__ = "scraped_data"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    content = Column(String)

Base.metadata.create_all(engine)

semaphore = asyncio.Semaphore(5)

async def fetch_url(url):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                save_data(url, data)

def save_data(url, content):
    session = Session()
    data = ScrapedData(url=url, content=content)
    session.add(data)
    session.commit()
    session.close()

async def main():
    urls = []
    while True:
        url = input("Введите URL для скрапинга (или 'q' для завершения): ")
        if url.lower() == 'q':
            break
        urls.append(url)

    tasks = [fetch_url(url) for url in urls]
    await asyncio.gather(*tasks)

    while True:
        await asyncio.sleep(3600)  # Подождать 1 час
        tasks = [fetch_url(url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
