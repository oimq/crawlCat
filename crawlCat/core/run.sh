python $CRAWLCAT_HOME/core/runCat.py \
-i $CRAWLCAT_HOME/demo/templates/info.json \
-k $CRAWLCAT_HOME/demo/templates/keywords.json \
-l $CRAWLCAT_HOME/demo/templates/layouts.json \
-o $CRAWLCAT_HOME/demo/templates/options.json \
-d $CHROME_DRIVER_PATH/chromedriver \
-e $CHROME_DRIVER_PATH/chrome_text_mode.crx \
-w $CRAWLCAT_HOME/demo/logs/ \
-s $CRAWLCAT_HOME/demo/outputs/final-[%time].json \
-n 1