from jSona import load, save
from os.path import join

def generate_keywords(isSave=False, cpath='./keywords.json') :
    pages = {
        i:v+1 for i,v in enumerate([
            10, 6, 4, 2, 1, 2, 1, 1, 1, 1
        ])
    }
    keywords = {
        'highwaymart_food':{
            "":{
                ["~0007000{0}?viewn=100&page={1}".format(i, j) for i in range(0, len(pages)) for j in range(1, pages[i])]
            }
        }
    }
    if isSave   : load(cpath, keywords)
    else        : return keywords

def generate_frames(isSave=False, cpath='./frames.json') :
    frames = {
        'highwaymart_food':{
            'url'  : 'https://www.highwaymart.co.kr/',
            'qurl' : 'https://www.highwaymart.co.kr/Mall/Category/~00070001?viewn=100&page=1',
            'lx' : [
                '//*[@id="goodsList"]/ul/li/a/@href'
            ],
            'li' : [
                False
            ],
            'ix' : {
                'name'  : '//*[@id="goodsForm"]/header/b',
                'code'  : '//*[@id="goodsForm"]/form/dl[1]/dd/b',
                'price_original'  : '//*[@id="goodsForm"]/form/dl[2]/dd/b',
                'price_discount'  : '//*[@id="goodsForm"]/form/dl[3]/dd/b/span',
                'image_thumbnail' : '//*[@id="goodsImages"]/header/img/@src',
                'image_content'   : '//*[@id="goodsUserDetail"]/p/img/@src'
            },
            'ii' : {
                'name' : True,
                'code' : True,
                'price_original'  : True,
                'price_discount'  : True,
                'image_thumbnail' : False,
                'image_content'   : False
            }
        },
    }
    if isSave   : load(cpath, frames)
    else        : return frames

def generate_config(isSave=False, cpath='./configs.json') :
    frames = {
        'highwaymart_food':{
            'CHAPCHA_CHK':False, 
            'MULTI_NEXTS':False,
            'RECUL_PAGES':False,
            'CRAWL_DELAY':2, 
            'SCRLL_TIMES':10, 
            'SCRLL_DELAY':4,
            'FIRST_EVENT':False,
            'PROGR_TBARS':True,
            'PGERROR_CHK':False,
            'FILTER_PAGE':[],
        },
    }
    if isSave   : load(cpath, frames)
    else        : return frames

if __name__=="__main__" :
    SETTING_PATH = './demo/'
    generate_keywords(isSave=True, cpath=join(SETTING_PATH, 'keywords.json'))
    generate_frames(isSave=True,   cpath=join(SETTING_PATH, 'frames.json'))
    generate_config(isSave=True,   cpath=join(SETTING_PATH, 'configs.json'))
