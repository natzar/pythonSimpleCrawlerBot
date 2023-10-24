# python Simple Crawler Bot
This script is a version of the one used at Domstry.com. You can use it to crawl the internet. It starts on the FIRST domain, links are extracted for the next run. It fetches domains, stores the data, and adds the links found in the current domain to the queue. It never ends.

As an example, right now it stores http_code, title, and description. It's very easy to add new fields and extract more details from each domain.

## Prerequisites

Ensure you have *Python >= 3.10* installed on your system. You can verify using:

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

Create a MySql database and import database.sql. 

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
python crawler.py
```
As a cronjob:
```bash
*/5 * * * * python /full/path/crawler.py
```
...

## Customize

In case you want to add new fields and extract additional data you would have to:

*Modify Database:*
- Add a new field in the table (Database)
- Modify *Domain Class* (ORM) - add new field and type

*Modify function fetch_domain_details function:*

It should return your new field. Feel free to add your code after BeautifulSoup, calculate your new field value, and return it, if the field exists in the database it will be stored.


## Support
Create an Issue to get support.

## Contribute

Pull requests are welcomed. 

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

