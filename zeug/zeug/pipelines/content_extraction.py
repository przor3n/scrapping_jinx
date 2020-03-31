[from scrapy.selector import Selector
from scrapy.exceptions import DropItem

from zeug.pages import get_page_object
from zeug.items import DownloadedItem
from zeug.env import (SPIDER_OUTPUT_ITEM, PAGE_MODULE, PAGE_OBJECT,
                      MONGO_DATABASE, MONGO_COLLECTION)

PO = get_page_object(PAGE_MODULE, PAGE_OBJECT)

from zeug.dongo import dongo_client

from lxml import html
import string
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords
import nltk


class ContentExtract(object):
    def process_item(self, item, spider):

        assert isinstance(item, DownloadedItem), "Must be the DownloadedItem"

        content = {}

        for name, xpath_selector in PO.extraction:

            content[name] = Selector(
                text=item.page_code).xpath(xpath_selector).get()

        item.content = content
        return item


class InsertMongo(object):
    db = None
    collection = None

    def open_spider(self, spider):
        self.db = dongo_client[MONGO_DATABASE]
        self.collection = self.db[MONGO_COLLECTION]

    def close_spider(self, spider):
        dongo_client.close()

    def process_item(self, item, spider):
        item.common_id = self.collection.insert_one(item.content).inserted_id
        return item


class NltkExtract(object) :
    """
      	

>>> fdist = nltk.FreqDist(['dog', 'cat', 'dog', 'cat', 'dog', 'snake', 'dog', 'cat'])
>>> for word in sorted(fdist):
...     print(word, '->', fdist[word], end='; ')
cat -> 3; dog -> 4; snake -> 1;

    """
    def T9_guessing() :
        pass
        #[w for w in wordlist if re.search('^[ghi][mno][jlk][def]$', w)]
        #['gold', 'golf', 'hold', 'hole']

    def remove_stopwords(l):
        stoplist = set(stopwords.words('english'))
        return [token for token in l if token not in stoplist]

    def strip_html(s):
        return str(html.fromstring(s).text_content())

    def remove_punctuation(s):
        return s.translate(dict.fromkeys(string.punctuation))

    def tokenize(s):
        return word_tokenize(s)

    def filter_alpha(l):
        return [word for word in l if word.isalpha()]

    def lowercase(l):
        return [word.lower() for word in l]

    def ngrams(l, size=2) :
        return ngrams(l, size)

    def some_strange_parsing():
        bgs_2 = nltk.bigrams(c_tokens)

        bgs_3 = nltk.trigrams(c_tokens)

        fdist = nltk.FreqDist(bgs_3)

        tmp = list()
        for k, v in fdist.items():
            tmp.append((v, k))
        tmp = sorted(tmp, reverse=True)

        for kk, vv in tmp[:]:
            print(vv, kk)
