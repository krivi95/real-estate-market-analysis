# Web scraping real estate data

## Introduction

This is the implementation of a web scraper used for getting information about real estate listings in Serbia from website [4zida.rs](https://www.4zida.rs/). It has been implemented in [Python 3.8](https://www.python.org/downloads/release/python-384/), using [Scrapy](https://scrapy.org/) library. Scraped data is being directly stored in [PostgreSQL container](https://hub.docker.com/_/postgres) via pipelines defined in scrapy project structure.

Data that has been scraped can be grouped in four categories:
1. Apartments for sale
2. Houses for sale
3. Apartments for rent
4. Houses for rent


## Project structure

In this repository you may find:
- `db_connetion.json` file - parameters to establish connection to postgres docker container.
- `proxy_list.txt` file - list of proxies through which web scraping will be perform (in order to avoid blacklisting your IP address from website). You can choose proxies on [free-proxy.cz](http://free-proxy.cz/en/)
- `\src` directory - contains implementation of web scraped, and db connectivity scripts.

In `\src` directory you may find:
- `db_initialization.py` file - script for creating new database and db structure in postgres container.
- `realestate` scrapy project

`\src\realestate` scrapy project has couple of spiders implemented and a pipeline for storing fetched data in database. More on this topic in following section: "How to run code?".

## How to run the scraper?

#### 1. Running postgres docker container
On how to set up postgres in docker container please refer to an [instruction](../database/).
After container has been up and running you can run `db_initialization.py` script, which will connect to that container, based on parameters from `db_connetion.json` file and create new database and tables.

#### 2. Running spiders
There are thre spiders implemented in this project:
- `4zida-apartments-sale` - scraping data about listed apartments for sale
- `4zida-houses-sale` - scraping data about listed houses for sale
- `4zida-real-estate-rent` - scraping data for both the apartments and the houses that are listed for rent.

In order to start any of the spiders you will have to `cd \src\realestate` and run the scrapy command e.g. `python -m scrapy crawl 4zida-apartments-sale`.

Implementation of pipeline for storring fetched data into db (postgres container) can be found in `\src\realestate\realestate\pipelines.py`.


#### 3. Avoid getting banned from website that you're scraping 
There are several thing that are being set up in order to avoid getting banned from website. If you go to `\src\realestate\realestate\settings.py` you will find which settings are being used:
- [scrapy-proxies](https://github.com/aivarsk/scrapy-proxies) library is being used to automatically route requests and rotate them through defined list of proxies (from `proxy_list.txt` file).
- [scrapy-user-agents](https://pypi.org/project/scrapy-user-agents/) library is used to automatically rotate different user agents when sending requests to the website.
- [scrapy's autothrottle option](https://docs.scrapy.org/en/latest/topics/autothrottle.html) is being enabled so the pace of sending requests is automatically adjusted based on website's server response time.
