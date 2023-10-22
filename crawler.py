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
import tldextract


# Constants
CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
DB_USERNAME = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "test"

SUBDOMAINS_ARE_OK = False # If you want to store domains, subdomains and www, set it to True
LIMIT_BATCH_DOMAINS = 100  # Number of domains fetched on each run
MAX_THREADS = 2 # Total number of domains fetched in parallel

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

def extract_domain_from_url(url):
    try:
        if SUBDOMAINS_ARE_OK:
            # Extract netloc (i.e., domain name) from the URL
            domain = urlparse(url).netloc
            return domain
        else:      
            extracted = tldextract.extract(url)        
            if not extracted.domain or not extracted.suffix:
                return None
            # Combine domain and suffix
            domain_with_suffix = f"{extracted.domain}.{extracted.suffix}"
            # Validate the domain format by parsing it. If this succeeds, then it's a valid domain format.
            domain = urlparse(f"https://{domain_with_suffix}").netloc       
            # Return the parsed domain (netloc)
            return domain
    except Exception as e:
        print(f"Error parsing URL {url}: {e}")
        return None

def fetch_domain_details(domain):
    headers = {"User-Agent": CHROME_USER_AGENT}
    try:
        response = requests.get('http://'+domain, headers=headers, timeout=5)
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title.string if soup.title else None
        description_tag = soup.find('meta', attrs={"name": "description"}) or soup.find('meta', attrs={"property": "og:description"})
        description = description_tag['content'][:255] if description_tag else None

		# Extract all links and convert to domains
        links = list(set([extract_domain_from_url(a['href']) for a in soup.find_all('a', href=True) if extract_domain_from_url(a['href'])]))

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

def upsert_domain_record(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
  
    if instance:       
        for key, value in defaults.items():
            setattr(instance, key, value)
        try:
            session.commit()
            print(f"Updated domain with ID: {instance.id} {instance.domain}")
        except Exception as e:
            print(f"Error during commit: {e}")
    else:
        print(f"Storing new domain with attributes {kwargs}")
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        session.add(instance)
        session.commit()
        print(f"New domain added with ID: {instance.id}")
        return instance

def store_domain_data(domain_name, data):
    session = Session()
    
    # Update current domain
    upsert_domain_record(
        session, 
        Domain, 
        defaults=data,
        domain=domain_name
    )

    # update_or_create for each link
    for link_domain in data['links']:
        link_instance = upsert_domain_record(session, Domain, domain=link_domain)
        if link_instance:
            print(f"Added new domain to the queue: {link_domain}")
        else:
            print(f"Failed to add domain: {link_domain} to the queue")
    
    session.close()

def process_domain(domain):
    data = fetch_domain_details(domain.domain)    
    if data:
        store_domain_data(domain.domain, data)

def main():
    display_cli_header()
    session = Session()
    if session.bind:
        print("Session is connected to the database!")
    else:
        print("Session is NOT connected!")

    domains = session.query(Domain).order_by(Domain.updated.asc()).limit(LIMIT_BATCH_DOMAINS).all()

    # Using ThreadPoolExecutor to multi-thread the crawling process
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(process_domain, domains)

def display_cli_header():
    line = "=" * 50
    name = "Package: pythonSimpleCrawlerBot"
    version = "Version: 1.0.1"
    author = "Author: Beto Ayesa, @betoayesa, beto.phpninja@gmail.com"
    license = "License: GPL3"
    description = "Fork it: https://github.com/natzar/pythonSimpleCrawlerBot"

    # ASCII art for demonstration
    logo = """
   
   _____ _                 __     ______                    __          ____        __ 
  / ___/(_____ ___  ____  / ___  / _____________ __      __/ ___  _____/ __ )____  / /_
  \__ \/ / __ `__ \/ __ \/ / _ \/ /   / ___/ __ `| | /| / / / _ \/ ___/ __  / __ \/ __/
 ___/ / / / / / / / /_/ / /  __/ /___/ /  / /_/ /| |/ |/ / /  __/ /  / /_/ / /_/ / /_  
/____/_/_/ /_/ /_/ .___/_/\___/\____/_/   \__,_/ |__/|__/_/\___/_/  /_____/\____/\__/  
                /_/                                                                    

    """

    print(line)
    print(logo)
    print(name)
    print(version)
    print(author)
    print(license)
    print(description)
    print(line)



if __name__ == '__main__':
    main()
