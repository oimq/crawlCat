#!/bin/sh

python $CRAWLCAT_HOME/core/runCat.py \
-i /home/park/datasets/crawlCat/facebook/templates/info.json \
-k /home/park/datasets/crawlCat/facebook/templates/keywords.json \
-l /home/park/datasets/crawlCat/facebook/templates/layouts.json \
-o /home/park/datasets/crawlCat/facebook/templates/options.json \
-d $CHROME_DRIVER_PATH/chromedriver \
-e $CHROME_DRIVER_PATH/chrome_text_mode.crx \
-w $CRAWLCAT_HOME/demo/logs/ \
-s $CRAWLCAT_HOME/demo/outputs/final-[%time].json \
-n 2