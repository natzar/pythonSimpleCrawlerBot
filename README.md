# python Simple Crawler Bot
This script is a version of the one used at Domstry.com. You can use it to crawl the internet. It fetches domains, stores the data, and adds the links found in the current domain to the queue.


## Prerequisites

Ensure you have Python 3.x installed on your system. You can verify using:

```bash
python --version
```

## Installation Steps

### 1. Clone the repository

```bash
git clone https://github.com/natzar/pythonSimpleCrawlerBot.git
cd pythonSimpleCrawlerBot
```

### 2. Database

Create a database and import database.sql. 

IMPORTANT: Insert the first domain to start with.


### 3. Install the dependencies

```bash
pip install -r requirements.txt
```
### 4. Configure

Edit crawler.py and look for constants sections:

```bash
MAX_THREADS = 1 (number of parallel domains fetched at the same time) 
DB_USER, DB_HOST, DB_PASSWORD = MySql Config Values

```
## Usage

Run it manually:
```bash
python3 crawler.py
```
As a cronjob:
```bash
*/5 * * * * python3 /full/path/crawler.py
```
Looks for ways to keep running a command in your system environment.

## Customize

In case you want to add new fields and extract additional data you would have to:
*Modify Database:*
- Add a new field in the table (Database)
- Modify *Domain Class* (ORM) - add new field and type

*Modify function fetch_domain_details function:*
It should return your new field. Feel free to add your code after beautifulsoup, calculate your new field value, and return it, it the field exists in the database it will be stored.


## Support
Contact @betoayesa on twitter/x
## Contribute

Pull requests accepted. The next thing is adding "plugins" so everyone can add any data 

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

