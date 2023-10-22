# pythonSimpleCrawlerBot
This script is a version of the one used at Domstry.com. You can use it to crawl the internet. It fetches domains, store the data, and adds the link to the queue.


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

## Usage

python3 crawler.py

Set a cronjob to maintain it running always.
```bash
* * * * * python3 crawler.py
``` 
Set MAX_THREADS 

## Contribute

Pull requests accepted. Next thing is adding "plugins" so everyone can add any data 

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

