import json
from lxml import html
import traceback
from selenium import webdriver

from familyCat import *
from readyCat import *

from time import sleep
from datetime import datetime
from random import uniform
from pyLog import Logger

logger = Logger(isWrite=False)
logger.set('name', 'crawlCat')
log = logger.log

class crawlCat() :
    def __init__(self, configs, driver_path :str, extensions_paths :list =[], max_pool :int =1000, write_path =None, mode='debug') :
        log("Hello, Welcome to crawlCat! - Cat initializes the module.")
        try :
            self.configs = configs
            self.browser = self.get_browser(driver_path, extensions_paths)
            self.claw    = self.set('claw')
            self.max_pool= max_pool
            self.pool    = []
            self.depth   = len(configs['layouts']['link_xpaths'])

            self.family  = Family()

            if mode == 'debug' : logger.set('level', 0)
        except Exception as e :
            self.error(e, "INIT", ex=True, cry=True)
        else :
            log("Driver is set. Don't remove the browser window until the end.")

        # self.response = None
        # self.source   = None
        # self.cats  = Cats()
        # self.cry   = cry
        # self.bars  = False
        # self.end   = False
        # self.history  = dict()

    def set(self, key) :
        if key == "claw" :
            if 'scroll' in self.configs['options'] and self.configs['options']['scroll']['count'] > 0:
                log("Cat chooses the [thick] claw!")
                return self.thick
            else :
                log("Cat chooses the [thin] claw!")
                return self.thin
    
    def error(self, e, msg="", ex=True, cry=True) :
        log("ERROR {} : {}".format(msg, e), 'e')
        if cry : traceback.print_exc()
        if ex  : exit()

    def get_browser(self, driver_path, extensions_paths) :
        chrome_options = webdriver.ChromeOptions()
        for ext_path in extensions_paths : chrome_options.add_extension(ext_path)
        return webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)

    # load the script
    def load(self, url) :
        try :
            if not self.browser : raise ValueError("There is no driver here.")
            self.browser.get(url) 
            return self.browser.page_source
        except ConnectionRefusedError as cre :
            self.error(cre, "LOAD - "+url, ex=False)
        except KeyboardInterrupt as kie :
            self.error(kie, "KEYBOARD")
        except Exception as e :
            self.error(e, "LOAD - "+url)

    def scroll(self, delay =0, ratio =0.95) :
        scroll_heights = [self.browser.execute_script("return document.body.scrollHeight"), 0]
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight*{});".format(ratio)); sleep(0.02)
        scroll_heights[1] = self.browser.execute_script("return document.body.scrollHeight")
        if scroll_heights[0] != scroll_heights[1] :
            if delay : sleep(delay*uniform(0.8, 1.2))
            return scroll_heights
        else :
            return False

    def thin(self, url) :
        try :
            page_source = self.load(url)
            log("Cat gets the {} size page from {}".format(len(page_source), url), 'd')
            return html.fromstring(page_source)
        except KeyboardInterrupt as kie :
            self.error(kie, "KEYBOARD")
        except Exception as e :
            self.error(e, "READ - "+url)

    def thick(self, url) :
        try :
            page_source = self.load(url)
            scroll_option = self.configs['options']['scroll']
            scroll_count, scroll_delay, scroll_ratio = scroll_option['count'], scroll_option['delay'], scroll_option['ratio']

            while scroll_count > 0 :
                scroll_heights = self.scroll(scroll_delay, scroll_ratio)
                if scroll_heights :
                    log("Cat scrolls the page, Bar heights : {} -> {}".format(*scroll_heights))
                    page_source += "\n"+self.load(url)
                    scroll_count -= 1
                else :
                    break
            log("Cat gets the {} size page from {}".format(len(page_source), url), 'd')
            return html.fromstring(page_source)
        except KeyboardInterrupt as kie :
            self.error(kie, "KEYBOARD")
        except Exception as e :
            self.error(e, "READ - "+url)

    def form(self, page_source, xpaths) :
        item = None
        if len(page_source) < 1 : log("There is no page source. skip.", "w")
        else :
            # Get items
            if type(xpaths) == type({}) :
                item = dict()
                for xkey in xpaths :
                    if type(xpaths[xkey]) == type("") : xpaths[xkey] = [xpaths[xkey]]
                    for xpath in xpaths[xkey] :
                        if "//" not in xpath : 
                            item[xkey] = [xpath]
                        else :
                            item[xkey] = [extr.replace('\t', '').strip() for extr in page_source.xpath(xpath)]
                        if len(item[xkey]) > 0 : break
                log("Success to getting the items : {}".format(str(item)), 'd')

            # Get links
            elif type(xpaths) == type("") or type(xpaths) == type("[]") :
                item = list()
                if type(xpaths) == type("") : xpaths = [xpaths]
                for xpath in xpaths :
                    item += page_source.xpath(xpath)
                log("Success to getting the links : {}".format(str(item)), 'd')

            # Unknown xpath type
            else :
                log("Unknown xpath type : {}, only possible str, list and dict".format(type(xpaths)), 'w')
        return item

    def quit(self) :
        log("Quit the crawlCat, Bye-nya~")
        self.browser.quit()

    # Is valid link?
    def isVaild(self, link) :
        if link in self.pool :
            return False
        else :
            if self.max_pool < len(self.pool) : self.pool.pop(0)
            self.pool.append(link)
            return True

    # Is Empty item?
    def isEmpty(self, item) :
        for v in item.values() :
            if len(v) > 0 : return False
        return True
        
    # lxi : link xpath index
    def crawl(self, url, loc) :
        try :          
            log("Cat crawl the url : {}".format(url), 'd')
            page_source = self.claw(url)

            # Get the links
            if self.depth > loc :
                log('Get the links, depth {} > {} loc'.format(self.depth, loc), 'd')
                links = self.form(page_source, self.configs['layouts']["link_xpaths"][loc])
                for link in links :
                    if self.isVaild(link) : self.crawl(link, loc+1)
            
            # Get the items
            ginx = self.configs['layouts']['get_indices'][loc]
            if ginx != -1 and ginx < len(self.configs['layouts']["item_xpaths"]):
                log('Get the items, get_indices {} at loc {}'.format(self.configs['layouts']['get_indices'][loc], loc), 'd')
                items = self.form(
                    page_source,
                    self.configs['layouts']["item_xpaths"][ginx]
                )
                if self.configs['options']['filter']['empty'] and self.isEmpty(items) : 
                    return log('Empty item occurs : {}'.format(items), 'd')

                # Store the Items
                self.family.add(items)
                log('Success to store items : {}'.format(items), 'd')

        except KeyboardInterrupt as ki :
            self.error(ki, "KEYBOARD", cry=False, ex=True)
        except Exception as e:
            traceback.print_exc()
            self.error(e, "CRAWL", cry=False, ex=False)

    def save(self, cpath) :
        if "[%time]" in cpath : cpath = cpath.replace("[%time]", str(datetime.now()).replace(" ", "-"))
        self.family.save(cpath)
        log("Cat saves the {} number of family to {}".format(self.family.size(), cpath))

if __name__=="__main__" :
    driver_path = "/home/park/myCrawling/drivers/chromedriver"
    extensions_paths = [
        "/home/park/myCrawling/drivers/chrome_text_mode.crx"
    ]
    config_path = '/home/park/myCrawling/modules/crawlCat/crawlCat/demo/templates/'
    parser = Parser(
        join(config_path, "info.json"),
        join(config_path, "keywords.json"),
        join(config_path, "layouts.json"),
        join(config_path, "options.json"),
    )
    
    # def __init__(self, configs, driver_path :str, extensions_paths :list =[], max_pool :int =1000, mode='debug') :
    cc = crawlCat(parser.get(), driver_path, extensions_paths)

    sample_urls = ['https://stocksnap.io/search/kitty']
    for url in sample_urls :
        cc.crawl(url, 0)
    
    cc.save("./crawl-output.json")
    cc.quit()

    # def setbars(self, lxn) :
    #     self.lxn  = lxn
    #     self.sbar = tqdm(bar_format="{desc}", desc="Initializing...", position=2)
    #     self.bars = [tqdm(total=1, position=i) for i in range(3,lxn+3)] 

    # def checkPgError(self, xpath) :
    #     page_status = self.form({'Page Error':xpath}, {'Page Error':False})['Page Error']
    #     if page_status and ('error' in page_status or '오류' in page_status) : return True
    #     else                                                                 : return False

    # def checkCaptcha(self) :
    #     if "validateCaptcha" in self.source :   return True
    #     else                                :   return False

    # def checkFilterW(self, xpath, fword) :
    #     words = self.form({'Filter Word':xpath}, {'Filter Word':False})['Filter Word']
    #     if len(list(filter(lambda w : fword in w, words))) > 0 : return True
    #     else                                                   : return False

