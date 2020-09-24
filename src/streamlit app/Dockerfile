FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

CMD streamlit run --server.port 8080 --server.enableCORS false app.py