import sys
import json
import traceback
import pprint
pp = pprint.pprint

def error(e, msg="") :
    print("ERROR {} : {}".format(msg, e))
    traceback.print_exc() 
    exit()

def loadJson(cpath) :
    try :
        with open(cpath) as openfile :
            return json.load(openfile)
        print("\Load success. {}\n".format(cpath))
    except Exception as e :
        error(e, "LOAD JSON")

def saveJson(cpath, table) :
    try :
        with open(cpath, 'w') as openfile :
            json.dump(table, openfile)
        print("\nSave cleaned data success. {}\n".format(cpath))
    except Exception as e :
        error(e, "SAVE JSON")

def generate_keywords(isSave=False, cpath='./keywords.json') :
    keywords = {
        "" : [""],
    }
    if isSave   : saveJson(cpath, keywords)
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
    if isSave   : saveJson(cpath, frames)
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
    if isSave   : saveJson(cpath, frames)
    else        : return frames

if __name__=="__main__" :
    # pp(generate_frames())
    generate_keywords(isSave=True)
    generate_frames(isSave=True)
    generate_config(isSave=True)
