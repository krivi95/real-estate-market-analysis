# Real estate analysis in Serbia

## Introduction

This repository contains a project representing full life cycle of implementing and deploying machine learning models from scratch to the production:

1. It starts from creting `web scraper` for getting an information about real estate listings in Serbia.  Scraped data is being directly stored in `PostgreSQL container` via pipelines defined in `scrapy` project structure. `Rotating proxies` and `rotating user agents` are used in a combination with a `autothrottling `(requests are automatically adjusted based on website's server response time) so we're not banned from a websites.

2. After that, `raw data has been cleaned`. Various ambiguous information is sorted out using common sense and some business knowlegde on real esatate market in Serbia and its cities. We're also `analysing, visualizing, extracting` an insights that are going to be valuable for implementing machine learning models.

3. When it comes to the modeling section, we're using `custom implementation` of:
    * `multiple linear regression with gradient descent` 
    * `multiclass (one-to-many) kernel SVM` 

4. When we trained the models, simple `web app` is created for demonstrating model capabilities to the end user. Application has been containerized with `Docker`. For creating a web app we're using `stramlit python library`.

5. `CI/CD` pipeline is created with `Travis CI` for building a container for our web application with docker and deploying it to a `Docker hub`.

Described project is implemented in [Python 3.8](https://www.python.org/downloads/release/python-385/). This implementation was done as project work on the course [Fiding the hidden knowledge (Machine learning)](https://www.etf.bg.ac.rs/fis/karton_predmeta/13M111PSZ-2013) on Master's degree in Software Engineering. 


## Project structure
In this repository under the `src` directory you may find separate projects for each of the steps that are previously described. Under those project, in `README.md` file, you may find the documentation, instructions on how to set up and use the code. Those project are:
- [database](./src/database) - contains the instruction on how to set up and run the perzistent PostgreSQL database container, scripts and backups.
- [web scraping](./src/web%20scraping) - contains the scrapy project and instrunctions on how to run the spiders for getting the data about real estate listings from the websites and storring them into the database.
- [data analysis](./src/data%20analysis) - contains the Jupyter notebooks for claening the raw dataset, analysing and visualizing data.
- [modeling](./src/modeling) - contains the implementation of a custom linear regression and SVM classification models, description how models work and Jupyter notebooks for training those models and additional notebooks for training a similar models from sklearn library as a baseline models for an evaluation and a comparison.
- [streamlit app](./src/streamlit%20app) - contains the simple containerized web application for demonstrating trained models.

In the root directory you may also find:
- `requirements.txt` file - Python 3.8 dependencies for running all of the projects. Please refer to the `README.md` documentation uder each project on how to run them.
- `.travis.yml` file - for `Travis CI` to automatically build and deploy the stramlit web app container directly to the Docker Hub, so users could pull the image and use it. 



