# def generate_keywords(isSave=False, cpath='/home/park/myCrawling/scripts/settings/instagram/keywords.json') :
#     keywords = {
#         "일상스타그램" : [""],
#     }
#     if isSave   : saveJson(cpath, keywords)
#     else        : return keywords

# def generate_frames(isSave=False, cpath='/home/park/myCrawling/scripts/settings/instagram/frames.json') :
#     frames = {
#         'instagram':{
#             'url'  : 'https://www.instagram.com',
#             'qurl' : 'https://www.instagram.com/explore/tags/[%]',
#             'lx' : [
#                 '//article/div/div/div/div/a/@href',
#                 [
#                     '//article/header/div[2]/div[1]/div[1]/a/@href',
#                     '//article/header/div[2]/div[1]/div[1]/span/a/@href'
#                 ],
#                 '//article/div/div/div/div/a/@href'
#             ],
#             'li' : [
#                 False,
#                 [
#                     False,
#                     False
#                 ],
#                 False
#             ],
#             'gi' : [
#                 False,
#                 False,
#                 True,
#                 True
#             ],
#             'ix' : {
#                 'user'    : [
#                     '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1',
#                     '//article/header/div[2]/div[1]/div[1]/span/a'
#                 ],
#                 'profile' : '//*[@id="react-root"]/section/main/div/header/section/div/span',
#                 'sns'     : 'instagram',
#                 'posts_num'    : '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span',
#                 'follower_num' : '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span',
#                 'followed_num' : '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span', 
#                 'post_alts'    : '//article/div/div/div/div/div/div/div/ul/li/div/div/div/div/img/@alt',
#                 'post_imgs'    : '//article/div/div/div/div/div/div/div/ul/li/div/div/div/div/img/@src',
#                 'post_desc'    : '//article/div[3]/div[1]/ul/div/li/div/div/div[2]/span',
#                 'comments_user' : '//article/div/div/ul/ul/div/li/div/div/div/h3/div/a',
#                 'comments_desc' : '//article/div/div/ul/ul/div/li/div/div/div/span'
                
#             },
#             'ii' : {
#                 'user'    : [True, True],
#                 'profile' : True,
#                 'sns'     : True,
#                 'posts_num'    : True,
#                 'follower_num' : True,
#                 'followed_num' : True,
#                 'post_alts' : False,
#                 'post_imgs' : False,
#                 'post_desc' : True,
#                 'comments_user' : True,
#                 'comments_desc' : True
#             }
#         },
#     }
#     if isSave   : saveJson(cpath, frames)
#     else        : return frames

# def generate_config(isSave=False, cpath='/home/park/myCrawling/scripts/settings/instagram/configs.json') :
#     frames = {
#         'instagram':{
#             'CHAPCHA_CHK':False, 
#             'MULTI_NEXTS':False,
#             'RECUL_PAGES':False,
#             'CRAWL_DELAY':2, 
#             'SCRLL_TIMES':60, 
#             'SCRLL_DELAY':4,
#             'FIRST_EVENT':7,
#             'PROGR_TBARS':True,
#             'PGERROR_CHK':"//body/div/div/div/div/h2//text()",
#             'FILTER_PAGE':False,
#         },
#     }
#     if isSave   : saveJson(cpath, frames)
#     else        : return frames

# if __name__=="__main__" :
#     # pp(generate_frames())
#     generate_keywords(isSave=True)
#     generate_frames(isSave=True)
#     generate_config(isSave=True)
