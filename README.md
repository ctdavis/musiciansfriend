This is a project that I did in order to figure out how to use MySQL in a Scrapy project with docker-compose -- it wasn't quite as straight forward as setting up a spider to interact with a containerized MongoDB, but as I have actually only ever used MySQL in a professional setting, it seemed worth it to take the time and work something out.

If you want to try it out, execute the following code:

    git clone git remote add origin https://github.com/ctdavis/musicdeals.git
    cd musicdeals

    docker-compose build
    docker-compose up -d

    # then, to check out the results:

    docker exec -it mysql-scrapy bash
    
    # the line above will put you in the MySQL container's terminal. From there, execute:

    mysql -uroot -hlocalhost -ppass

    # now you'll be inside a mysql client

    use musiciansfriend;
    select count(*) from musiciansfriend;

DISCLAIMER: This scraper and any data that may be captured through its use are for demonstration purposes only
