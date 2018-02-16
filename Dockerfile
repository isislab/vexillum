FROM python:2.7

RUN apt-get update && apt-get install -y python-dev python-pip sqlite3 
WORKDIR /opt/
COPY ./ /opt/
RUN pip install -r requirements.txt
CMD python serve.py
