# Real estate data analysis

In this section, first, we will do the data cleaning of the raw, scraped data; sort out various ambiguous information using common sense and some business knowlegde on real esatate market in Serbia and its cities.

Upon finishing data cleaning, cleaned dataset is being saved back into postgres database using [sqlalchemy](https://www.sqlalchemy.org/) python library.

Now when we have cleaned dataset, we will dive deeper into undertanding our data, extract some useful information from it, analyse and visualize it, in order to better understand local real estate market and to prepare the data for building various pricing models.


# Project structure
Data cleaning and analysis is done in [Jupyter Notebook](https://jupyter.org/).

In this directory, you will find four jupyter notebooks:
- `data_cleaning.ipynb` - for handling missing values, detecting outliers, ... 
- `data_cleaning_location.ipynb` - for determining the correct location (city and city district) using geographical knowledge, for wrong and ambgious real estate locations.
- `real_estate_analysis.ipynb` - looking into our cleaned dataset and trying to answer research questions about real estate market.
- `real_estate_visualization.ipynb` - visualizing distribution and segmentation of some attributes on properties: location, price, year of construction, sales/rental numbers... 


# How to view jupyter notebooks?

You can try to open the notebooks directly on github and it should be able to render the notebooks directly there.

If github rendering doesn't work (e.g. some JS features of the notebooks), you can paste the link of individual notebook, or of the whole repository, into [Jupyter's online nbviewer](https://nbviewer.jupyter.org/).
You can also directly view notebooks using online nbviewer by clicking on the links bellow:
- [data_cleaning.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/data%20analysis/data_cleaning.ipynb)
- [data_cleaning_location.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/data%20analysis/data_cleaning_location.ipynb)
- [real_estate_analysis.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/data%20analysis/real_estate_analysis.ipynb)
- [real_estate_visualization.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/data%20analysis/real_estate_visualization.ipynb)

You can also clone the repository and view the notebooks locally with jupyter notebook library.