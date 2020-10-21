# System libraries
import sys
import traceback
from pprint import pprint as pp
from time import sleep
from random import randint as rint
from tqdm import tqdm

# User libraries
from readyCat import Parser
from crawlCat import crawlCat
from jSona import load, save
from pyLog import Logger

def create_urls(info, keywords) :
    print(info, keywords)
    return [info['query'].replace("[%mk]",mk).replace("[%sk]",sk) for mk in keywords for sk in keywords[mk]]
            
if __name__=='__main__' :
    parser  = Parser()
    configs = parser.get_configs()
    options = parser.get_options()
    urls    = create_urls(configs['info'], configs['keywords'])
    logger  = Logger()
    logger.set('name', 'runCat')
    log     = logger.log
    log("Successfully load arguments {}".format(str(parser)))

    driver_path= parser.get_driver_path()
    cc      = crawlCat(configs=configs, driver_path=driver_path, **options)
    log("Cat successfully ready for crawling. There are {} urls.".format(len(urls)))
    try :
        pass
    except KeyboardInterrupt as kie :
        pass
    except Exception as e :
        log(str(e))
        traceback.print_exc()
    finally :
        cc.save("./final-[%time].json")
        cc.quit()
