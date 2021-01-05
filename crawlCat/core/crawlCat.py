import json
from lxml import html, etree
import traceback
from selenium import webdriver

from familyCat import *
from readyCat import *

from time import sleep
from datetime import datetime
from random import uniform
from pyLog import Logger

logger = Logger(isWrite=False)
log = logger.log

class crawlCat() :
    def __init__(self, configs, driver_path :str, extensions_paths :list =[], max_pool :int =1000, write_path =None, mode ='debug', name ='crawlCat') :
        log("Hello, Welcome to crawlCat! - Cat initializes the module.")
        try :
            # crawlCat set
            self.configs = configs
            self.browser = self.get_browser(driver_path, extensions_paths)
            self.claw    = self.set('claw')
            self.max_pool= max_pool
            self.pool    = []
            self.depth   = len(configs['layouts']['link_xpaths'])
            self.family  = Family()
            # Logger set
            logger.set('name', name)
            if write_path : logger.set_write(write_path)
            if mode == 'debug' : logger.set('level', 0)
        except Exception as e :
            self.error(e, "INIT", ex=True, cry=True)
        else :
            log("Chrome driver is set. Don't remove the browser's window until the end.")

        # self.response = None
        # self.source   = None
        # self.cats  = Cats()
        # self.cry   = cry
        # self.bars  = False
        # self.end   = False
        # self.history  = dict()

    def set(self, key) :
        if key == "claw" :
            if self.configs['options']['scroll']['count'] > 0:
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
    def load(self, url, delay =0) :
        try :
            if not self.browser  : raise ValueError("There is no driver here.")
            if not "http" in url : url = self.configs['info']['prefix'] + url
            self.browser.get(url) 
            self.delay(delay)
            return self.browser.page_source
        except ConnectionRefusedError as cre :
            self.error(cre, "LOAD - "+url, ex=False)
        except KeyboardInterrupt as kie :
            self.error("Detect the ctrl+c.", "KEYBOARD", cry=False)
        except Exception as e :
            self.error(e, "LOAD - "+url)

    def delay(self, sec) :
        if sec > 0 : return sleep(sec*uniform(0.8, 1.2))
        else : return None

    def scroll(self, delay =0, ratio =0.95) :
        scroll_heights = [self.browser.execute_script("return document.body.scrollHeight"), 0]
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight*{});".format(ratio)); sleep(0.02)
        scroll_heights[1] = self.browser.execute_script("return document.body.scrollHeight")
        if scroll_heights[0] != scroll_heights[1] :
            self.delay(delay)
            return scroll_heights
        else :
            return False

    def thin(self, url, delay =0) :
        try :
            page_source = self.load(url, delay)
            log("Cat gets the {} size page from {}".format(len(page_source), url), 'd')
            return html.fromstring(page_source)
        except KeyboardInterrupt as kie :
            self.error("Detect the ctrl+c.", "KEYBOARD", cry=False)
        except Exception as e :
            self.error(e, "READ - "+url)

    def thick(self, url, delay =0) :
        try :
            page_source = self.load(url, delay)
            scroll_option = self.configs['options']['scroll']
            scroll_count, scroll_delay, scroll_ratio = scroll_option['count'], scroll_option['delay'], scroll_option['ratio']

            while scroll_count > 0 :
                scroll_heights = self.scroll(scroll_delay, scroll_ratio)
                if scroll_heights :
                    log("Cat scrolls the page, Bar heights : {} -> {}".format(*scroll_heights), 'd')
                    page_source += "\n"+self.browser.page_source
                    scroll_count -= 1
                else :
                    break
            log("Cat gets the {} size page from {}".format(len(page_source), url), 'd')
            return html.fromstring(page_source)
        except KeyboardInterrupt as kie :
            self.error("Detect the ctrl+c.", "KEYBOARD", cry=False)
        except Exception as e :
            self.error(e, "READ - "+url)

    def form(self, page_sources, xpaths) :
        item = None
        if len(page_sources) < 1 : log("There is no page source. skip.", "w")
        else :
            for page_source in page_sources :
                # Get items
                if type(xpaths) == type({}) :
                    item = dict()
                    for xkey in xpaths :
                        if type(xpaths[xkey]) == type("") : xpaths[xkey] = [xpaths[xkey]]
                        for xpath in xpaths[xkey] :
                            if "//" not in xpath : 
                                item[xkey] = [xpath]
                            else :
                                item[xkey] = page_source.xpath(xpath)
                            if len(item[xkey]) > 0 : 
                                if item[xkey] and ("<Element" in str(item[xkey][0])) :
                                    print("->")
                                    item[xkey] = page_source.xpath(xpath+"/descendant::*/text()")
                                    print(item[xkey])
                                break
                    log("Success to getting the items : {}".format(str(item)), 'd')

                # Get links
                elif type(xpaths) == type("") or type(xpaths) == type([]) :
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
    
    # Create the init urls
    def create_urls(self) :
        return [
            self.configs['info']['query'].replace("[%mk]",mk).replace("[%sk]",sk) 
            for mk in self.configs['keywords'] for sk in self.configs['keywords'][mk]
        ]

    def run(self) :
        urls = self.create_urls()
        log("Cat start to crawling {} number of urls".format(len(urls)), 'd')
        for url in urls : self.crawl(url, 0)

    def isPass(self, url, page_sources) :
        if self.configs['options']['filter']['url'] :
            for furl in self.configs['options']['filter']['url'] :
                if url in furl or furl in url : return True
        if self.configs['options']['filter']['page'] :
            for xp, kw in self.configs['options']['filter']['page'] :
                for cw in page_sources[0].xpath(xp) :
                    if kw in cw : return True
        return False

    def isStop(self, page_sources) :
        if self.configs['options']['check']['chapcha'] :
            for xp, kw in self.configs['options']['check']['chapcha'] :
                if kw in self.form(page_sources, {"box":xp})['box'] :
                    return "STOP : Chapcha page {}".format(kw)
        if self.configs['options']['check']['error'] :
            for xp, kw in self.configs['options']['check']['error'] :
                if kw in self.form(page_sources, {"box":xp})['box'] :
                    return "STOP : Error page {}".format(kw)
        return False
        
    # lxi : link xpath index
    def crawl(self, url, loc) :
        try :          
            log("Cat crawl the url : {}, Current location : {}".format(url, loc), 'd')
            page_sources = [self.claw(url, self.configs['options']['delay']['total']+self.configs['options']['delay']['first'])] \
                if loc == 0 and self.configs['options']['delay']['first'] > 0 else \
                [self.claw(url, self.configs['options']['delay']['total'])]

            # Pass or Stop page
            isPass, isStop = self.isPass(url, page_sources), self.isStop(page_sources)
            if isPass : 
                return
            elif isStop :
                while True :
                    if input("{} occur, Type 'g' or 'go' for retry.".format(isStop)) in ['g', 'go'] : break
                return self.crawl(url, loc)

            # Get the items
            ginx, items = self.configs['layouts']['get_indices'][loc], None
            if ginx > -1 and ginx < len(self.configs['layouts']["item_xpaths"]):
                log('Get the items, get_indices {} at loc {}'.format(self.configs['layouts']['get_indices'][loc], loc), 'd')
                items = self.form(
                    page_sources,
                    self.configs['layouts']["item_xpaths"][ginx]
                )
                if self.configs['options']['filter']['empty'] and self.isEmpty(items) : 
                    log('Empty item occurs : {}'.format(items), 'd')
                else :
                    # Store the Items
                    self.family.add(items)
                    log('Success to store items to family : {}'.format(items), 'd')

            # Get the links
            if self.depth > loc :
                log('Get the links, depth {} > {} loc'.format(self.depth, loc), 'd')
                links = self.form(page_sources, self.configs['layouts']["link_xpaths"][loc])
                del page_sources, items, url, ginx
                for link in links :
                    if self.isVaild(link) : self.crawl(link, loc+1)
            
        except KeyboardInterrupt as ki :
            self.error("Detect the ctrl+c.", "KEYBOARD", cry=False)
        except Exception as e:
            traceback.print_exc()
            self.error(e, "CRAWL", cry=False, ex=False)

    def save(self, cpath) :
        if "[%time]" in cpath : cpath = cpath.replace("[%time]", str(datetime.now()).replace(" ", "-"))
        self.family.save(cpath)
        log("Cat saves the {} number of family to {}".format(self.family.size(), cpath))

from os.path import join

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

