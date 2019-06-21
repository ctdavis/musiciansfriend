This repo is for the purpose of demonstrating how to deploy a Scrapy web scraper and a MySQL database together, with docker-compose (the repo's name comes from the fact that the scraper used to operate on musiciansfriend.com, which unsurprisingly, turned out to be a bad choice -- now it scrapes quotes.toscrape.com, the same website used in Scrapy's documentation). In order to test it out, clone the repo and execute the following command:

    docker-compose up --build -d

Once MySQL is ready, you can execute the following line:

    docker run -it --network=musiciansfriend_scrapy_mysql_net mysql mysql -uroot -ppass -hdb

And when you're in the MySQL interpreter, execute something like this:

    use quotes;
    select * from quotes;
