FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /movie_shop
COPY requirements.txt /movie_shop/
RUN pip install -r requirements.txt

COPY . /movie_shop/
