"""
    pythonSimpleCrawlerBot v.1.0
    
    Copyright (C) 2023 Beto Ayesa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Author:
        Beto Ayesa, @betoayesa, beto.phpninja@gmail.com
"""


from sqlalchemy import create_engine, Column, Integer, String, DateTime, UniqueConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse


# Constants
CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

Base = declarative_base()

class Domain(Base):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True)
    domain = Column(String, unique=True)
    http_code = Column(Integer)
    title = Column(String(255))
    description = Column(String(255))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('domain'),)

# Set up the database
DATABASE_URL = "sqlite:///crawler.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_domain_from_url(url):
    try:
        # Extract netloc (i.e., domain name) from the URL
        domain = urlparse(url).netloc
        return domain
    except Exception as e:
        print(f"Error parsing URL {url}: {e}")
        return None

def get_details(domain):
    headers = {"User-Agent": CHROME_USER_AGENT}
    try:
        response = requests.get(domain, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title.string if soup.title else None
        description_tag = soup.find('meta', attrs={"name": "description"}) or soup.find('meta', attrs={"property": "og:description"})
        description = description_tag['content'] if description_tag else None

        # Extract all links and convert to domains
        links = [get_domain_from_url(a['href']) for a in soup.find_all('a', href=True) if get_domain_from_url(a['href'])]

        return {
            'http_code': response.status_code,
            'title': title,
            'description': description,
            'links': links
        }
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred for {domain}: {http_err}")
        return None
    except Exception as e:
        print(f"Error fetching details for {domain}: {e}")
        return None

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def save_data(domain_name, data):
    session = Session()
    domain = session.query(Domain).filter_by(domain=domain_name).first()
    if domain:
        domain.http_code = data['http_code']
        domain.title = data['title']
        domain.description = data['description']

        for link_domain in data['links']:
            get_or_create(session, Domain, domain=link_domain)

    session.commit()
    session.close()

def save_data(domain_name, data):
    session = Session()
    domain = session.query(Domain).filter_by(domain=domain_name).first()
    if domain:
        domain.http_code = data['http_code']
        domain.title = data['title']
        domain.description = data['description']

        for link in data['links']:
            new_domain = Domain(domain=link)
            session.add(new_domain)

    session.commit()
    session.close()

def crawl_domain(domain):
    data = get_details(domain.domain)
    if data:
        save_data(domain.domain, data)

def main():
    session = Session()
    domains = session.query(Domain).order_by(Domain.updated.asc()).all()

    # Using ThreadPoolExecutor to multi-thread the crawling process
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(crawl_domain, domains)

if __name__ == '__main__':
    main()
