import json
from lxml import html
import traceback
from selenium import webdriver
from crawlCat.familyCat import Cats, Kitty
from time import sleep
from datetime import datetime
from tqdm import tqdm
import pprint
pp = pprint.pprint

class crawlCat() :
    def __init__(self, driver_path, driver='Chrome', cry=True) :
        self.setDriver(driver_path)
        self.response = None
        self.source   = None
        self.cats  = Cats()
        self.cry   = cry

    def error(self, e, msg="") :
        print("ERROR {} : {}".format(msg, e))
        traceback.print_exc()

    def crying(self, items) :
        if self.cry :
            try :
                if   type(items) == type([]) : print("Go through link : {}".format(len(items)), end="")
                elif type(items) == type({}) : print("Cat Crawl the items : {}".format(len(items)), end="\n")
                print(datetime.now())
                pp(items)
            except Exception as e:
                self.error(e, 'CRY')

    def setDriver(self, driver_path, driver='Chrome') :
        if driver=='Chrome' : 
            self.browser = webdriver.Chrome(executable_path=driver_path)
            print("Driver is set. don't remove the browser window.")
        else :
            self.browser = None
            print("Un-supportable format : {}".format(driver))

    def read(self, url, delay=0, scroll_time=0, scroll_delay=0) :
        try :
            if not self.browser : raise Exception("There is no driver here.")
            self.browser.get(url) 
            self.source   = self.browser.page_source

            if delay > 0 : sleep(delay)
            while scroll_time > 0 : 
                last_height = self.browser.execute_script("return document.body.scrollHeight")
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight*0.8);"); scroll_time -= 1
                if scroll_delay > 0 : sleep(scroll_delay); 
                self.source  += '\n'+self.browser.page_source
                if last_height == self.browser.execute_script("return document.body.scrollHeight") : break
                
            self.response = html.fromstring(self.source)

        except Exception as e :
            self.error(e, "READ")
            self.source   = None
            self.response = None
        finally :
            return self.response

    # [] : link xpaths, {} : item xpaths
    def form(self, xpaths, istext, url=False) :
        try :
            if self.response == None : raise Exception("There are no responses.")

            item = None
            
            if   type(xpaths) == type({}) and type(xpaths) == type(istext) :
                item = dict()
                if url : item['url'] = [url]
                for xkey in xpaths :
                    if   type(xpaths[xkey]) == type("") :
                        if "//" not in xpaths[xkey] :
                            item[xkey] = xpaths[xkey]
                        else :
                            item[xkey] = [content.replace('\t', '').strip() \
                                for content in self.response.xpath(xpaths[xkey]+("//text()" if istext[xkey] else ""))]
                                
                    elif type(xpaths[xkey]) == type([]) :
                        for xinx in range(len(xpaths[xkey])) :
                            item[xkey] = [content.replace('\t', '').strip() \
                                for content in self.response.xpath(xpaths[xkey][xinx]+("//text()" if istext[xkey][xinx] else ""))]
                            if len(item[xkey]) > 0 : break

            elif type(xpaths) == type([]) and len(xpaths) == len(istext) :
                item = list()
                for xinx in range(len(xpaths)) :
                    if "//" not in xpaths[xinx] :
                        item.append(xpaths[xinx])
                    else :
                        item = item + self.response.xpath(xpaths[xinx]+("//text()" if istext[xinx] else ""))
            
            if item : self.crying(item)
            return item

        except Exception as e :
            self.error(e, "FORM")
            return None

    def trim(self, **kwargs) :
        default = {
            'CHAPCHA_CHK':False, 'MULTI_NEXTS':False, 'RECUL_PAGES':False,
            'CRAWL_DELAY':0, 'SCRLL_TIMES':0, 'SCRLL_DELAY':0,
        }
        return {k:kwargs[k] if k in kwargs else default[k] for k,dv in default.items()}

    # ix = dictionary
    # ii = dictionary
    # lx = lists
    # li = lists
    def crawl(self, url, ix, ii, lx, li, prefix, **kwargs) :
        craw = self.trim(**kwargs)
        self.read(
            url, 
            delay=craw['CRAWL_DELAY'], 
            scroll_time=craw['SCRLL_TIMES'], 
            scroll_delay=craw['SCRLL_DELAY']
        )

        # Capchat check
        if craw['CHAPCHA_CHK'] and self.checkCaptcha() :
            while True :
                isSolved = input("Captcha founded. After solved them, type 's' or 'solved'.")
                if set(isSolved)&set("s", "solved") : break
            self.crawl(url, ix, ii, lx, li, prefix, **kwargs)
            return

        # Crawling
        else :
            if len(lx) > 0 :   # If link_xpath are exist, get all next page sources
                if craw['RECUL_PAGES'] : self.crawl(url, ix, ii, lx[1:], li[1:], prefix, **kwargs)  # Go though the next page - Recursion
                links = self.form(lx[:1], li[:1])
                if links :
                    if craw['MULTI_NEXTS'] and links : links = [links[-1]] if len(links) == 2 else links
                    for link in links :         # Go thought the inside pages.
                        if prefix not in link  : link = prefix + link
                        if craw['RECUL_PAGES'] : self.crawl(link, ix, ii, lx, li, prefix, **kwargs)
                        else                   : self.crawl(link, ix, ii, lx[1:], li[1:], prefix, **kwargs)
                    
                else : return           # none link -> just return

            else :                      # If there are no link_xpath, now it is time for getting items!
                items = self.form(ix, ii, url)
                if items : self.cats.add(Kitty(**items))
                

    def checkCaptcha(self) :
        if "validateCaptcha" in self.source :   return True
        else                                :   return False

    def save(self, cpath) :
        self.cats.save(cpath)

    def quit(self) :
        self.browser.quit()