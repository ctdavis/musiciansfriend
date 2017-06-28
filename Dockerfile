FROM python:3.5

COPY . /scrapy

WORKDIR /scrapy

RUN pip install lxml scrapy mysqlclient

ENTRYPOINT ["scrapy"]
CMD ["crawl","musiciansfriend"]
