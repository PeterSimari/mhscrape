# mhscrape
Monster Hunter Wiki scraper

In the directory of the project, you'll have to setup your own virtual environment.
I'll eventually add a requirements.txt, but you mainly just need python3 and scrapy installed to be able to run this.

## Running a spider:
Its easy to run a spider. In the directory of the file just type 
```
'scrapy crawl monsters'
```
You can also return this as a json file by using the command:
```
scrapy crawl monsters -o output.json
```
This is the ideal way to test, because we will be importing this json into a database at a later time.
I may update the names of these, but you can see what the name of the spider is under the spider folder structure.

## Scraping a site in a shell
Running a scrape more directly so you can work with the data from the site is easy too, just use:
```scrapy shell '{URL}'``` - in a case for the large mosnters I'm scraping: ```"scrapy shell 'https://monsterhunter.fandom.com/wiki/Rathalos'"```
This opens an interactive shell that you can mess around with the data in.
Feel free to just run one of the commands from the spider to see how that works, example:
```'response.css("h2[data-source='Name']::text").get()'```
Should return ```'Rathalos'```


type quit() to exit this.
