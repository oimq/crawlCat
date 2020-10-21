DEFAULT_CONFIG = {
    "keys":[
        "info", "keywords", "layouts", "options"
    ],
    "info":{
        "url":"",
        "query":"",
        "prefix":""
    },
    "keywords":{
        "":[
            "",
        ],
    },
    "layouts":{
        "get_indices":[],
        "link_xpaths":[],
        "item_xpaths":[]
    },
    "options":{
        'check':{
            'stop':[], #[[check_xpath, text]]
            'error':[], #[[check_xpath, text]]
        },
        'delay':{
            'first':0,
            'total':0,
        },
        'scroll':{
            'count':0,
            'delay':0,
        },
        'filter':{
            "empty":True,
            'url':[], #[urls]
            'page':[], #[[filter_xpath, text]]
        }
    }
}

descrtiption = '''
Welcome to crawlCat!
Cat crawls the any forms of web sites.
You just give those files to cat.
info.json, keywords.json, layouts.json, options.json 
'''

epilog = '''
Cat automatically start scraping sites when you give them!
'''

import argparse
from jSona import load
import traceback

class Parser :
    def __init__(self) :
        self.parser = argparse.ArgumentParser(
            description=descrtiption,
            epilog=epilog,
            allow_abbrev=True,
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
        )
        self.append_arguments()
        try :
            self.ns = self.parser.parse_args()
            self.configs = {
                DEFAULT_CONFIG['keys'][i]:self.set(DEFAULT_CONFIG['keys'][i], path)
                for i, path in enumerate([self.ns.info, self.ns.keywords, self.ns.layouts, self.ns.options])
            }
        except Exception as e:
            traceback.print_exc()
            print("ERROR : Parser initializing", e)

    def append_arguments(self) :
        self.parser.add_argument(
            '-n', '--num-proc',
            help="Number of Crawler Processes",
            metavar="number",
            type=int,
            nargs="?",
            required=False,
            default=1
        )
        self.parser.add_argument(
            '-e', '--extensions-paths',
            help="Paths for Extensions of Chrome",
            metavar="path, ...",
            type=str,
            nargs="*",
            required=False,
            default=[]
        )
        self.parser.add_argument(
            '-mp', '--max-pool',
            help="Set maximum pool size of history (default :1000)",
            metavar="N",
            type=int,
            nargs="?",
            required=False,
            default=1000
        )
        self.parser.add_argument(
            '--mode',
            help="Set debug mode, It would effect the logs.",
            metavar="debug",
            type=str,
            nargs="?",
            required=False,
            default='debug'
        )
        self.parser.add_argument(
            '-w', '--write-path',
            help="Write the prints to the logs.",
            metavar="path",
            type=str,
            nargs="?",
            required=False,
            default=""
        )
        required = self.parser.add_argument_group('required arguments')
        required.add_argument(
            '-i', '--info',
            help="Path for info.json",
            metavar="path",
            type=str,
            nargs="?",
            required=True,
        )
        required.add_argument(
            '-k', '--keywords',
            help="Path for keywords.json",
            metavar="path",
            type=str,
            nargs="?",
            required=True
        )
        required.add_argument(
            '-l', '--layouts',
            help="Path for layouts.json",
            metavar="path",
            type=str,
            nargs="?",
            required=True
        )
        required.add_argument(
            '-o', '--options',
            help="Path for options.json",
            metavar="path",
            type=str,
            nargs="?",
            required=True
        )
        required.add_argument(
            '-d', '--driver-path',
            help="Path for Chrome driver",
            metavar="path",
            type=str,
            nargs="?",
            required=True
        )
        
        
    def set(self, key, path) :
        return self.compl(load(path, cry=False), DEFAULT_CONFIG[key])
    
    def compl(self, data, default) :
        if type(default) == type({}) :
            for k in default :
                if not k       : continue
                elif k in data : data[k] = self.compl(data[k], default[k])
                else           : data[k] = default[k]
            return data
        else :
            if data : return data
            else    : return default
    
    def get_configs(self) :
        return self.configs
    
    def get_driver_path(self) :
        return self.ns.driver_path

    def get_num_proc(self) :
        return self.ns.num_proc

    def get_options(self) :
        return {
            'extensions_paths'  : self.ns.extensions_paths,
            'max_pool'          : self.ns.max_pool,
            'mode'              : self.ns.mode,
            'write_path'        : self.ns.write_path
        }

    def __str__(self) :
        return str(self.ns)

from os.path import join
from pprint import pprint as pp

if __name__=="__main__" :
    config_path = '/home/park/myCrawling/modules/crawlCat/crawlCat/demo/templates/'
    parser = Parser()
    pp(parser.get())
    