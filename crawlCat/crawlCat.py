import json
from lxml import html
import traceback
from selenium import webdriver
from familyCat import Cats, Kitty
from time import sleep
from datetime import datetime
from tqdm import tqdm
from random import randint as rint
from functools import reduce
import pprint
pp = pprint.pprint

class crawlCat() :
    def __init__(self, driver_path, driver='Chrome', cry=True) :
        self.setDriver(driver_path)
        self.response = None
        self.source   = None
        self.cats  = Cats()
        self.cry   = cry
        self.bars  = False
        self.end   = False
        self.history  = dict()

    def error(self, e, msg="", ex=True, cry=True) :
        print("ERROR {} : {}".format(msg, e))
        self.end = True
        if cry : traceback.print_exc()
        if ex  : exit()

    def crying(self, items) :
        if self.cry :
            try :
                print(datetime.now())
                if   type(items) == type([]) : print(" - Go Through Links : {}".format(len(items)), end="\n")
                elif type(items) == type({}) : print(" - Cat Crawl the Items : {}".format(len(items)), end="\n")
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

    def read(self, url, delay=0, scroll_time=0, scroll_delay=0, cry=True) :
        try :
            if not self.browser : raise ValueError("There is no driver here.")
            self.browser.get(url) 

            if delay > 0 : sleep(delay)
            self.source = self.browser.page_source

            last_height = 0
            while scroll_time > 0 : 
                if last_height == self.browser.execute_script("return document.body.scrollHeight") : break
                last_height = self.browser.execute_script("return document.body.scrollHeight")
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight*0.95);"); scroll_time -= 1
                if scroll_delay > 0 : sleep(scroll_delay*rint(8, 12)/10)
                self.source  += '\n'+self.browser.page_source
                if self.cry : print("Scrolling : {} times now.".format(scroll_time))
                if self.cry : print("Last ScrollHeight : {}, Current ScrollHeight : {}".format(
                    last_height, self.browser.execute_script("return document.body.scrollHeight")
                ))
            
            
            self.response = html.fromstring(self.source)
        except ConnectionRefusedError as cr :
            self.error(cr, "READ", cry=False, ex=True)
        except KeyboardInterrupt as ki :
            self.error(ki, "KEYBOARD", cry=False, ex=True)
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
                        try :
                            if "//" not in xpaths[xkey] :
                                item[xkey] = xpaths[xkey]
                            else :
                                item[xkey] = [content.replace('\t', '').strip() \
                                    for content in self.response.xpath(xpaths[xkey]+("//text()" if istext[xkey] else ""))]
                        except TypeError :
                            print(xpaths[xkey])
                                
                    elif type(xpaths[xkey]) == type([]) :
                        for xinx in range(len(xpaths[xkey])) :
                            item[xkey] = [content.replace('\t', '').strip() \
                                for content in self.response.xpath(xpaths[xkey][xinx]+("//text()" if istext[xkey][xinx] else ""))]
                            if len(item[xkey]) > 0 : break

            elif type(xpaths) == type([]) and len(xpaths) == len(istext) :
                if xpaths and type(xpaths[0])==type([]) : xpaths = reduce(lambda x,y:x+y, xpaths)
                if istext and type(istext[0])==type([]) : istext = reduce(lambda x,y:x+y, istext)
                item = list()
                for xinx in range(len(xpaths)) :
                    if "//" not in xpaths[xinx] :
                        item.append(xpaths[xinx])
                    else :
                        item = item + self.response.xpath(xpaths[xinx]+("//text()" if istext[xinx] else ""))
            
            self.crying(item)
            return item

        except KeyboardInterrupt as ki :
            self.error(e, "KEYBOARD", cry=False, ex=True)
        except Exception as e :
            self.error(e, "FORM", ex=True)

    def trim(self, **kwargs) :
        default = {
            'CHAPCHA_CHK':False, 'MULTI_NEXTS':False, 'RECUL_PAGES':False, 'PGERROR_CHK':False,
            'CRAWL_DELAY':0, 'SCRLL_TIMES':0, 'SCRLL_DELAY':0, 'FIRST_EVENT':False, 'FILTER_PAGE':[],
        }
        if 'lxn' in kwargs : self.setbars(kwargs['lxn'])
        return {k:kwargs[k] if k in kwargs else default[k] for k,dv in default.items()}

    def setbars(self, lxn) :
        self.lxn  = lxn
        self.sbar = tqdm(bar_format="{desc}", desc="Initializing...", position=2)
        self.bars = [tqdm(total=1, position=i) for i in range(3,lxn+3)] 

    # ix = dictionary, item_xpath
    # ii = dictionary, item_istext
    # gi = lists, get_items
    # lx = lists, link_xpath
    # li = lists, link_istext
    def crawl(self, url, ix, ii, gi, lx, li, prefix, craw, times=0) :
        try :
            if self.end or times > 10 : return
            if self.bars : self.sbar.set_description(desc="We visit the URL : {}".format(url))

            # pp([url, ix, ii, gi, lx, li])

            if craw['FIRST_EVENT'] : 
                if self.cry : 
                    while not input("If you ready, enter the 'go' or 'g' : ") in ['go', 'g'] : pass
                self.read(
                    url, 
                    delay=craw['CRAWL_DELAY']+(craw['FIRST_EVENT'] if type(craw['FIRST_EVENT'])==type(0) else 0), 
                    scroll_time=craw['SCRLL_TIMES'], 
                    scroll_delay=craw['SCRLL_DELAY']
                )
                craw['FIRST_EVENT'] = False
            else :
                self.read(
                    url, 
                    delay=craw['CRAWL_DELAY'], 
                    scroll_time=craw['SCRLL_TIMES'], 
                    scroll_delay=craw['SCRLL_DELAY']
                )
            
            # Page check - is it okay?
            if craw['CHAPCHA_CHK'] and self.checkCaptcha() :
                while True :
                    isSolved = input("Captcha founded. After solved them, type 's' or 'solved'.")
                    if set(isSolved)&set("s", "solved") : break
                self.crawl(url, ix, ii, gi, lx, li, prefix, craw)
                return
            if craw['PGERROR_CHK'] and self.checkPgError(craw['PGERROR_CHK']) : 
                wait_seconds = rint((times*10+10)*0.8, times*10+10*1.2)
                if self.cry : print("Page is stoped... after wait a {} seconds, then restart the crawl.".format(wait_seconds))
                sleep(wait_seconds)
                self.crawl(url, ix, ii, gi, lx, li, prefix, craw, times+1)
                return
            if craw['FILTER_PAGE'] :
                for filter_meta in craw['FILTER_PAGE'] :
                    if self.checkFilterW(filter_meta[0], filter_meta[1]) : 
                        if self.cry : print("Page is filtered : {}".format(url))
                        return
            
            # Crawling
            if len(lx) > 0 :   # If link_xpath are exist, get all next page sources
                links = self.form(lx[:1], li[:1])
                if craw['RECUL_PAGES'] : self.crawl(url, ix, ii, gi[1:], lx[1:], li[1:], prefix, craw) # Dig also root url
                if links :
                    links = list(set(links)) # Remove duplicated links
                    if self.bars: self.bars[self.lxn-len(lx)].reset(); self.bars[self.lxn-len(lx)].total = len(links)
                    if craw['MULTI_NEXTS'] and links : links = [links[-1]] if len(links) == 2 else links
                    for link in links :         # Go thought the inside pages.
                        if prefix not in link  : link = prefix + link
                        self.crawl(link, ix, ii, gi[1:], lx[1:], li[1:], prefix, craw)
                        if self.bars : self.bars[self.lxn-len(lx)].update(1)
            
            # Store the Items
            if len(gi)>0 and gi[0] :
                self.cats.add(Kitty(**self.form(ix, ii, url)))

        except KeyboardInterrupt as ki :
            self.error(ki, "KEYBOARD", cry=False, ex=True)
            raise ki                
        except Exception as e:
            traceback.print_exc()
            self.error(e, "CRAWL", cry=False, ex=False)

    def checkPgError(self, xpath) :
        page_status = self.form({'Page Error':xpath}, {'Page Error':False})['Page Error']
        if page_status and ('error' in page_status or '오류' in page_status) : return True
        else                                                                 : return False

    def checkCaptcha(self) :
        if "validateCaptcha" in self.source :   return True
        else                                :   return False

    def checkFilterW(self, xpath, fword) :
        words = self.form({'Filter Word':xpath}, {'Filter Word':False})['Filter Word']
        if len(list(filter(lambda w : fword in w, words))) > 0 : return True
        else                                                   : return False

    def save(self, cpath) :
        self.cats.save(cpath)

    def quit(self) :
        if self.bars : 
            for bar in self.bars : bar.close()
        self.browser.quit()
        self.brower = None