scrapy crawl $SPIDER -s JOBDIR=crawls



SPIDER='webpage_spider'
SPIDER_OUTOUT_ITEM='LinkItem' # 'DownloadedItem'
PAGE_MODULE='wykop'
PAGE_OBJECT='WykopXML'  # 'Wykop

# write all links to database
scrapy crawl $SPIDER -s JOBDIR=wykop_links


SPIDER='links'
SPIDER_OUTPUT_ITEM='DownloadedItem'
PAGE_OBJECT='Wykop'

# crawl through all the links and download stuff
scrapy crawl $SPIDER -s JOBDIR=wykop_pages
