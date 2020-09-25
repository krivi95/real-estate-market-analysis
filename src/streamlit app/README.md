# Streamlit web application

In this section we're using a [Streamlit python library](https://www.streamlit.io/) to create a simple web application demostrating trained custom regression and classification models.

For each of the models the user would have to specify the input parameters after which the model gives the prediction:
- City district
- Area
- Number of rooms
- Heating type
- Apartment floor
- Number of the floor in a building
- Is it registered
- ...

Data that user has entered through the app needs to be standardized and one-hot-encoded before it enters the model. All of the column transformers and the fitted model object itself, are previously being serialized and export with [pickle](https://docs.python.org/3/library/pickle.html) library and on the app initialization we're loading those objects.

# Project structure

Under this project you will find:
- `models` directory - containing serialized, pickled column transformers and model objects for both the multiple linear regression and kernel multiclass SVM.
- `app.py` file - main application file that is an entry point to our streamlit library
- `settings.py` file - all of the settings and parameters our app needs to run with trained models.
- `svm.py` file - custom implementation of multiclass SVM, which needs to be imported before we unpickle our SVM model object.
- `model_utils.py` file - contains various functionalities such as populating DataFrame with raw user imports, transforming those inputs, making a prediction...
- `Dockerfile` file - for containerizing our application.
- `requirements.txt` file - python 3.8 requirements to run the application.

# Running docker container

First you will need to build the docker image (this may take a while, because it's downloading all the python libraries from requirements.txt file): `docker build -t psz-real-estete-models .`

Now, you can run docker container with following command:
`docker run -p 8080:8080 psz-real-estete-models`.
Port 8080 is exposed, so you would be able to deploy it and access the application from a browser.

When docker container is running on port 8080, you can access it with the browser:
`http://localhost:8080/`.

# Running streamlit app locally

It is recommended that you create new [virtual environment](https://docs.python.org/3/tutorial/venv.html): python3 -m venv python-env

Then you would need to activate that newly created python environment:
- On Windows: `python-env\Scripts\activate.bat`
- On Linux: `source python-env/bin/activate`

Once you have your python environment activated, first you would need to download all necessary python modules with pip. There is requirements.txt file for that. You can use the following command to automatically download all dependencies: `pip install -r requirements.txt`

When the download is completed, you can run streamlit app with: `streamlit run app.py`