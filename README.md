# crawlCat

##### Crawling and scraping the web pages with selenium and chrome module

for installing, requires are below : 

* selenium : https://github.com/SeleniumHQ/Selenium

* chrome driver that matches your chrome version : https://chromedriver.chromium.org/downloads

* tqdm : https://github.com/tqdm/tqdm

* jSona : https://github.com/oimq/jSona

***

### Installation
```
pip3 install crawlCat-master
```

***

### Projects

crawlCat is consisted by two parts

* crawlCat : Crawl and scrap module for websites.

* familyCat : Having the data structure (key-values)


demo has that configure and run the crawlCat.

* tarGetor : Configuration of crawlCat module.

* runCat : Run the crawling and scraping

***

### Configuration

We defined the configurations of crawlCat at demo/tarGetor.py

```
 * configs example
{
    'identifier':{
        'CHAPCHA_CHK':bool, # If chapcha occur, immediately stops.
        'MULTI_NEXTS':bool, # If there are two links, select last one.
        'RECUL_PAGES':bool, # Crawl again to url which make link not item.
        'CRAWL_DELAY':int,  # Seconds.
        'SCRLL_TIMES':int,  # Scrolling if the scroll space is left.
        'SCRLL_DELAY':int,  # Seconds.
        'FIRST_EVENT':bool, # Stops when first comes.
        'PROGR_TBARS':bool, # Show the Progress bars
        'PGERROR_CHK':bool, # If a page has 'error' or '오류', skips. 
        'FILTER_PAGE':[('xpath', 'keyword')], # if xpath item has keyword, skips.
    },
}

 * Frames example
{
    "identifier" : {
        'url' : 'https://www.cat.com/',
        'qurl' : https://'www.cat.com/search?keyword=[%]&parameter=yahon'
        "link_xpaths": [ "xpath", ... ], 
        "link_istext": [ bool,    ... ], 
        "item_xpaths": { "field" : "xpath", ... }, 
        "item_istext": { "field" : bool,    ... }
    },
}

 * Keywords example
{
    "main" : [ "sub0", "sub1", ... ],
}


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
