FROM python:3.6-slim

COPY . /root

WORKDIR /root

RUN pip install flask gunicorn sklearn numpy joblib flask_wtf pandas