# Web scraping real estate data

## Introduction

This is the implementation of a web scraper used for getting information about real estate listings in Serbia from website [4zida.rs](https://www.4zida.rs/). It has been implemented in [Python 3.8](https://www.python.org/downloads/release/python-384/), using [Scrapy](https://scrapy.org/) library. Scraped data is being stored is [PostgreSQL container](https://hub.docker.com/_/postgres).

Data that has been scraped can be grouped in four categories:
1. Apartments for sale
2. Houses for sale
3. Apartments for rent
4. Houses for rent


## Project structure

In this repository you may find:
- `db_connetion.json` file - parameters to establish connection to postgres docker container.
- `proxy_list.txt` file - list of proxies through which web scraping will be perform (in order to avoid blacklisting your IP address from website). You can choose proxies on [free-proxy.cz](http://free-proxy.cz/en/)
- `\scr` directory - contains implementation of web scraped, and db connectivity scripts.

In `\scr` directory you may find:
- `db_initialization.py` file - script for creating new database and db structure in postgres container.
- `realestate` scrapy project

`\src\realestate` scrapy project has couple of spiders implemented and a pipeline for storing fetched data in database. More in "How to run code?" section.

## How to run the scraper?

#### 1. Running postgres docker container
On how to set up postgres in docker container please refer to an [instruction](../database/). 
