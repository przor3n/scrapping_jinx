export SPIDER='webpage_spider'
export SPIDER_OUTOUT_ITEM='LinkItem' # 'DownloadedItem'
export PAGE_MODULE='wykop'
export PAGE_OBJECT='WykopXML'  # 'Wykop

# write all links to database
scrapy crawl $SPIDER -s JOBDIR=wykop_links
