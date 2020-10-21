# System libraries
import sys
import traceback
from pprint import pprint as pp
from time import sleep
from random import randint as rint
from multiprocessing import Process
from copy import deepcopy

# User libraries
from readyCat import Parser
from crawlCat import crawlCat
from jSona import load, save
from pyLog import Logger

def run(configs, options, driver_path, save_path, name ="crawlCat") :
    cc      = crawlCat(configs=configs, driver_path=driver_path, name=name, **options)
    log("Cat {} successfully ready for crawling".format(name))
    try :
        cc.run()
    except KeyboardInterrupt as kie :
        pass
    except Exception as e :
        log(str(e))
        traceback.print_exc()
    finally :
        cc.save(save_path)
        cc.quit()

# Multi-Processing functions
def equally_divide(l, n) :
    newl, q, r = list(), len(l)//n, len(l)%n
    for i in range(n) : ci = q+(1 if i < r else 0); newl.append(l[:ci]); del(l[:ci])
    return newl

def configs_divide(divided_keywords, n, old_configs) :
    new_configs_list = list()
    for i in range(n) :
        new_configs = deepcopy(old_configs)
        new_configs['keywords'] = dict()
        for keyword in divided_keywords[i] :
            mk, sk = keyword.split('[%-%]')
            if mk in new_configs['keywords'] : new_configs['keywords'][mk].append(sk)
            else : new_configs['keywords'][mk] = [sk]
        new_configs_list.append(new_configs)
    return new_configs_list

if __name__=='__main__' :
    parser  = Parser()
    configs = parser.get_configs()
    options = parser.get_options()
    driver_path = parser.get_driver_path()
    save_path   = parser.get_save_path()
    
    logger  = Logger(wpath=options['write_path'], isWrite=True) if options['write_path'] else Logger()
    logger.set('name', 'runCat')
    log     = logger.log
    log("Successfully load the arguments : {}".format(str(parser)))

    num_proc = parser.get_num_proc()
    if num_proc == 1 :
        run(configs, options, driver_path)
    elif num_proc > 1 :
        all_keywords = ["{}[%-%]{}".format(mk, sk) for mk in configs['keywords'] for sk in configs['keywords'][mk]]
        if len(all_keywords) < num_proc :
            log("Number of Process argument {} is greater than length of all keywords {}".format(num_proc, len(all_keywords)))
            num_proc = len(all_keywords)
        log("The {} Processes are prepared to start".format(num_proc))
        divided_keywords = equally_divide(all_keywords, num_proc)
        divided_configs  = configs_divide(divided_keywords, num_proc, configs)
        process_list = [
            Process(target=run, args=(divided_configs[i], options, driver_path, save_path, "cCat {}".format(i),))
            for i in range(len(divided_configs))
        ]
        log("The {} Processes are start now".format(len(process_list)))
        for proc in process_list :
            proc.start()
        for proc in process_list :
            proc.join()
        log("All {} Processes are successfully done the crawlings".format(len(process_list)))
    else :
        log("Number of Process argument is {}, that should be >= 1".format(num_proc), 'e')

    
