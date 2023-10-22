# pythonSimpleCrawlerBot
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

python3 crawler.py

Set a cronjob to maintain it running always.
```bash
* * * * * python3 crawler.py
``` 
## Customize

In case you want to add new fields and extract additional data you would have to:
- add a new field in the table (database)
- modify Domain Class (add new field and type)
- fetch_domain_details function should return your new field


## Support
Contact @betoayesa on twitter/x
## Contribute

Pull requests accepted. The next thing is adding "plugins" so everyone can add any data 

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

