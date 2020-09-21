import sys
import traceback
from pprint import pprint as pp

from jSona import load, save

def error(e, msg="", cry=True, ex=True) :
    print("ERROR {} : {}".format(msg, e))
    if cry : traceback.print_exc() 
    if ex  : exit()

def generate_keywords(isSave=False, cpath='./keywords.json') :
    keywords = {
        "" : [""],
    }
    if isSave   : save(cpath, keywords)
    else        : return keywords

def generate_frames(isSave=False, cpath='./frames.json') :
    frames = {
        'LABEL':{
            'url'  : 'https://',
            'qurl' : 'https://search?text=',
            'lx' : [
                'XPATH',
            ],
            'li' : [
                False,
            ],
            'ix' : {
                'FIELD'     : 'XPATH',
            },
            'ii' : {
                'FIELD'     : True,
            }
        },
    }
    if isSave   : save(cpath, frames)
    else        : return frames

def generate_config(isSave=False, cpath='./configs.json') :
    frames = {
        'LABEL':{
            'CHAPCHA_CHK':False, 
            'MULTI_NEXTS':False,
            'RECUL_PAGES':False,
            'CRAWL_DELAY':5, 
            'SCRLL_TIMES':7, 
            'SCRLL_DELAY':1,
            'PROGR_TBARS':True,
        },
    }
    if isSave   : save(cpath, frames)
    else        : return frames

if __name__=="__main__" :
    # pp(generate_frames())
    generate_keywords(isSave=True)
    generate_frames(isSave=True)
    generate_config(isSave=True)
