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

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, UniqueConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# Constants
CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "test"

MAX_THREADS = 3 # parallel execution

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
DATABASE_URL = "mysql+mysqlconnector://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME

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
        response = requests.get('http://'+domain, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title.string if soup.title else None
        description_tag = soup.find('meta', attrs={"name": "description"}) or soup.find('meta', attrs={"property": "og:description"})
        description = description_tag['content'] if description_tag else None

		# Extract all links and convert to domains
        links = list(set([get_domain_from_url(a['href']) for a in soup.find_all('a', href=True) if get_domain_from_url(a['href'])]))

        title = str(title)
        description = str(description)

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

def update_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        print(instance.domain)  # Replace 'attribute_name' with the actual attribute you want to print.

    if instance:
        print(f"Found existing record for {model} with attributes {kwargs}")
        for key, value in defaults.items():
            setattr(instance, key, value)
        print("before commit...")
        try:
            session.commit()
            print(f"Updated record for {model} with ID: {instance.id}")
        except Exception as e:
            print(f"Error during commit: {e}")
    else:
        print(f"Creating new record for {model} with attributes {kwargs}")
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        session.add(instance)
        session.commit()
        print(f"New record created with ID: {instance.id}")
        return instance

def save_data(domain_name, data):
    session = Session()
    
    # Use update_or_create for the current domain
    domain = update_or_create(
        session, 
        Domain, 
        defaults={'http_code': data['http_code'], 'title': data['title'], 'description': data['description']},
        domain=domain_name
    )

    # Use update_or_create for each link
    for link_domain in data['links']:
        link_instance = update_or_create(session, Domain, domain=link_domain)
        if link_instance:
            print(f"Processed link domain: {link_domain}")
        else:
            print(f"Failed to process link domain: {link_domain}")
    
    session.close()

def crawl_domain(domain):
    data = get_details(domain.domain)
    print(f"Data fetched for {domain.domain}: {data}")
    if data:
        save_data(domain.domain, data)

def main():
    print_cli_header()
    session = Session()
    if session.bind:
        print("Session is connected to the database!")
    else:
        print("Session is NOT connected!")

    domains = session.query(Domain).order_by(Domain.updated.asc()).all()

    # Using ThreadPoolExecutor to multi-thread the crawling process
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(crawl_domain, domains)
def print_cli_header():
    line = "=" * 50
    name = "   Your Script Name"
    version = "Version: 1.0.0"
    description = "This script does amazing things!"

    # ASCII art for demonstration
    logo = """
    __   __    _    _
   |  \ /  \  / \  / \
   |   V    |/ _ \| 0 |
   |_ _| \__/ \_/ \_/
    """

    print(line)
    print(logo)
    print(name)
    print(version)
    print(description)
    print(line)



if __name__ == '__main__':
    main()
