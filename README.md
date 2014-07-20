profcrawl
=========

Quick and dirty ratemyprof scraper: Because their data analysis leaves much to be desired.

Usage
-----

To scrape data for some given query at ratemyprof run the following command from the root of the project's source folder:

    $ scrapy crawl query.profs -t json -o output_file.json -a query=query_file

The query_file is a text file containing the target website's domain name, and a full search query URL for the spider to begin its crawl. For example:

    ratemyprofessors.com
    http://www.ratemyprofessors.com/SelectTeacher.jsp?the_dept=All&sid=1484

To run some basic keyword analysis on the scraped data, run:

    $ python keywords.py -p output_file.json -t target_folder

Keyword analysis requires the python's Distiller package: https://github.com/FranciscoCanas/Distiller