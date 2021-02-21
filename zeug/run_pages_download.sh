PAGE_MODULE='wykop'
SPIDER='links'
SPIDER_OUTPUT_ITEM='DownloadedItem'
PAGE_OBJECT='Wykop'

# crawl through all the links and download stuff
scrapy crawl $SPIDER -s JOBDIR=wykop_pages
