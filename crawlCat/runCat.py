guide = '''
This script is for Crawling(Scraping).

At first, we need item & link xpaths and keywords. 
For that, you should make the frames file, keywords file and configs file (json format).

 * Frames example
{
    "identifier" : {
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

This script also argues that driver path and output path. Then, it would be start the crawling(scraping).

Option description
 *  -l , -log           :  show all progressed logs. (default)
 *  -lp, -log-progress  :  show only progress bar.
 *  -li, -log-items     :  show only crawled items.
 *  -wt, -wait-time     :  deside the wait time. it should be time > 100. (default : 0)

System arguments
<usage> <driver> <output> <identifier> <frames> <keywords> <configs> <options>

Necessory libraries
 * crawlCat
 * tqdm

'''

# System libraries
import sys
import json
import traceback
import pprint
from time import sleep
from random import randint as rint
from tqdm import tqdm
pp = pprint.pprint

# User libraries
from crawlCat import crawlCat

def error(e, msg="", ise=True) :
    print("ERROR {} : {}".format(msg, e))
    traceback.print_exc() 
    if ise : exit()

def loadJson(cpath) :
    try :
        with open(cpath) as openfile :
            return json.load(openfile)
        print("\Load success. {}\n".format(cpath))
    except Exception as e :
        error(e, "LOAD JSON", ise=True)

if __name__=='__main__' :
    if set(["-help", "-h"]) & set(sys.argv) :     
        print(guide); exit()
    if len(sys.argv) < 7 :
        print("Wrong arguments : {}. Guide is available on option -h or -help".format(sys.argv[1:])); exit()

    show = ""
    if   set(['-lp', '-log-progress']) & set(sys.argv)        : show += 'p'
    elif set(['-li', '-log-items']) & set(sys.argv)           : show += 'i'
    elif set(['-l' , '-log']) & set(sys.argv)                 : show += 'pi'
    wait = 0
    if set(['-wt']) & set(sys.argv) : wait += int(sys.argv[sys.argv.index('-wt')+1])

    # Configuration of crawlCat
    dpath, opath, identifier = sys.argv[1], sys.argv[2], sys.argv[3]

    frames, keywords, configs = loadJson(sys.argv[4]), loadJson(sys.argv[5]), loadJson(sys.argv[6])
    prefix, qurl, link_xpaths, link_istext, item_xpaths, item_istext = frames[identifier].values()
    urls = ["{}{}{}".format(qurl, mainkw, subkw) for mainkw in keywords for subkw in keywords[mainkw]]

    # Crawling
    crawl = crawlCat(dpath, cry=(True if "i" in show else False))
    if 'p' in show : pbar = tqdm(total=len(urls))
    try :
        for uinx in range(len(urls)) :
            crawl.crawl(
                urls[uinx], item_xpaths, item_istext, link_xpaths, link_istext, prefix=prefix,
                **configs[identifier]) 
            if 'p' in show : pbar.update(1)
            if wait > 0 : sleep(rint(int(wait*0.8), int(wait*1.2))/1000)
        crawl.save(opath)
    except Exception as e :
        error(e, "FOUNDED", False)
        crawl.save(opath)
        input() # wait!
    finally :    
        crawl.quit()
        if 'p' in show : pbar.close()
        exit()