# crawlCat

##### Crawling and scraping the web pages with selenium and chrome module

for installing, requires are below : 

* selenium : https://github.com/SeleniumHQ/Selenium

* chrome driver that matches your chrome version : https://chromedriver.chromium.org/downloads

* jSona : https://github.com/oimq/jSona

* pyLog : https://github.com/oimq/pyLog

***

### Installation

before you start, please install the jSona from above url

```
pip3 install crawlCat-master
```

***

### Projects

crawlCat is consisted by two parts.

* crawlCat : Crawl and scrap module for target websites.

* familyCat : Data structure (key-values).

* runCat : Run the crawlCat by command line.

***

### Configuration

For using runCat, that need 4 configuration files : info.json, keywords.json, layouts.json, options.json

We defined the configuration files in demo/templates/

##### We will migrate configurations to database

```

***

### Example

* Setting Scripts

```code
python tarGetor.py
```

* Output
```code
SAVE SUCCESS TO [ ./demo/keywords.json ]
SAVE SUCCESS TO [ ./demo/frames.json ]
SAVE SUCCESS TO [ ./demo/configs.json ]
```

<br/><br/>

* Start Crawling
```
python ./demo/runCat.py ./chromedriver ./demo/scraped.json stocksnap \
    ./demo/frames.json ./demo/keywords.json ./demo/configs.json \
    -wt 1000 -li
```

* Output
```
Cat Crawl the items : 4
2020-07-10 13:09:17.344892
{'alt': ['yellow flower close up'],
 'src': ['https://cdn.stocksnap.io/img-thumbs/960w/yellow-flower_GWT9JVALSV.jpg'],
 'tags': ['yellow',
          'flower',
          ...
          'plants',
          'vegetation',
          'beautiful'],
 'url': ['https://stocksnap.io//photo/yellow-flower-GWT9JVALSV']}

Save data success. ./demo/scraped.json

100%|█████████████████| 48/48 [06:25<00:00,  8.04s/it]
```

***

### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.
