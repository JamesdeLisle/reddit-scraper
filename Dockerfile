FROM python:3.10-alpine

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY reddit_scraper /app/reddit_scraper
COPY main.py /app/main.py

CMD python /app/main.py