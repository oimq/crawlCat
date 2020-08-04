# crawlCat

##### Crawling and scraping the web pages with selenium and chrome module

for installing, requires are below : 

* selenium : https://github.com/SeleniumHQ/Selenium

* chrome driver that matches your chrome version : https://chromedriver.chromium.org/downloads

* tqdm : https://github.com/tqdm/tqdm

***

### Projects

crawlCat is consisted by three parts

* crawlCat : Crawl and scrap module for websites.

* familyCat : Has the data structure (key-values)

* lookCat : Configuration of crawlCat module.

* runCat : Run the crawling and scraping

***

### Configuration

```
 * Frames example
{
    "ccat" : {
        'site' : 'www.crawlcat.com',
        'qurl' : 'www.crawlcat.com?keyword='
        "link_xpaths": [ "xpath", ... ], 
        "link_istext": [ bool, ... ], 
        "item_xpaths": { "field" : "xpath", ... }, 
        "item_istext": { "field" : bool, ... }
    },
}

 * Keywords example
{
    "main" : [ "sub0", "sub1", ... ],
}

 * configs example
 {
    "identifier": {
        "CHAPCHA_CHK": false, 
        "MULTI_NEXTS": false, 
        "CRAWL_DELAY": 1, 
        "SCRLL_TIMES": 1, 
        "SCRLL_DELAY": 2
    }
}
```

***

### Example

* Script
```code
python runCat driver_path output_path ccat frames_path keywords_path configs_path options
```

* Output
```code
Go through link : [~]
Cat Crawl the items : {~}
```

***

### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.