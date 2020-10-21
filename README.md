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

Before run the command, set the enviornment variables

```
export $CRAWLCAT_HOME=your crawlCat path/crawlCat-master/crawlCat
export CHROME_DRIVER_PATH=your Chrome driver path
```

```
python $CRAWLCAT_HOME/core/runCat.py \
-i $CRAWLCAT_HOME/demo/templates/info.json \
-k $CRAWLCAT_HOME/demo/templates/keywords.json \
-l $CRAWLCAT_HOME/demo/templates/layouts.json \
-o $CRAWLCAT_HOME/demo/templates/options.json \
-d $CHROME_DRIVER_PATH/chromedriver \
-e $CHROME_DRIVER_PATH/chrome_text_mode.crx \
-w $CRAWLCAT_HOME/demo/logs/ \
-s $CRAWLCAT_HOME/demo/outputs/final-[%time].json \
-n 4
```

* Output
```
...
{'alt': ['yellow flower close up'],
 'src': ['https://cdn.stocksnap.io/img-thumbs/960w/yellow-flower_GWT9JVALSV.jpg'],
 'tags': ['yellow',
          'flower',
          ...
          'plants',
          'vegetation',
          'beautiful'],
 'url': ['https://stocksnap.io//photo/yellow-flower-GWT9JVALSV']}
...
INFO  2020-10-21 18:40:28.061336 cCat 0 | Cat saves the 0 number of family to /home/park/myCrawling/modules/crawlCat/crawlCat/demo/outputs/final-2020-10-21-18:40:28.061190.json
INFO  2020-10-21 18:40:28.061391 cCat 0 | Quit the crawlCat, Bye-nya~
```

***

### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.
