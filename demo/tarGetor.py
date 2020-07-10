from jSona import jSona
from os.path import join
sj = jSona().saveJson

def generate_keywords(isSave=False, cpath='./keywords.json') :
    keywords = {
        "food ":  [  
             "cooking", "fruit"
        ],
    }
    if isSave   : sj(cpath, keywords)
    else        : return keywords

def generate_frames(isSave=False, cpath='./frames.json') :
    frames = {
        'stocksnap':{
            'url'  : 'https://stocksnap.io/',
            'qurl' : 'https://stocksnap.io/search/[%]',
            'lx' : [
                '//*[@id="main"]/a/@href'
            ],
            'li' : [
                False
            ],
            'ix' : {
                'src'  : '//*[@id="main"]/div[1]/div[1]/figure/img/@src',
                'alt'  : '//*[@id="main"]/div[1]/div[1]/figure/img/@alt',
                'tags' : '//*[@id="main"]/div[2]/div[2]/div/a'
            },
            'ii' : {
                'src'  : False,
                'alt'  : False,
                'tags' : True
            }
        },
    }
    if isSave   : sj(cpath, frames)
    else        : return frames

def generate_config(isSave=False, cpath='./configs.json') :
    frames = {
        'stocksnap':{
            'CHAPCHA_CHK':False, 
            'MULTI_NEXTS':False,
            'RECUL_PAGES':False,
            'CRAWL_DELAY':2, 
            'SCRLL_TIMES':10, 
            'SCRLL_DELAY':4,
            'FIRST_EVENT':False,
            'PROGR_TBARS':True,
            'PGERROR_CHK':False,
            'FILTER_PAGE':[('//head/meta[3]/@content', 'shutterstock')],
        },
    }
    if isSave   : sj(cpath, frames)
    else        : return frames

if __name__=="__main__" :
    SETTING_PATH = './demo/'
    generate_keywords(isSave=True, cpath=join(SETTING_PATH, 'keywords.json'))
    generate_frames(isSave=True,   cpath=join(SETTING_PATH, 'frames.json'))
    generate_config(isSave=True,   cpath=join(SETTING_PATH, 'configs.json'))
