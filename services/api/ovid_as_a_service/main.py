import random

from whoosh.index import open_dir
from whoosh.qparser.default import QueryParser
from whoosh.query import Term
from whoosh.qparser import MultifieldParser

class OvidAsAService():
    def __init__(self):
        self.index = self._init_index()
        self.credits = "This A.S. Kline translation of Ovid's The Metamorphoses was scraped from University of Virginia Library's Ovid Collection. See more: https://ovid.lib.virginia.edu/about.html. Labor ipse voluptas."
    
    # INT FUNCTIONS
    def _init_index(self):
        return open_dir("index")

    def _get_results(self, query, fields, filter=None):
        query = str(query)
        qp = MultifieldParser(fields, schema=self.index.schema)
        q = qp.parse(query)
        search  = self.index.searcher()
        response = search.search(q, limit=None, filter=filter, sortedby='line')
        results = [dict(hit) for hit in response]

        if len(results) <= 0:
            return {'message': 'no results!'}
        
        results_obj = {
            'count': len(results),
            'results': results, 
            'credits': self.credits
        }
        return results_obj

    # EXT FUNCTIONS
    def query_text(self, query: str):
        return self._get_results(query, ['chapter_name', 'text'])      

    def query_book(self, book_num: int, chapter, query):
        if (int(book_num) <= 0) or (int(book_num) > 16):
            return {'error': 'Book number must be between 1 and 16'}
        else: 
            if chapter and not query:
                filter_chap = Term("chapter", str(chapter))
                return self._get_results(book_num, ['book'], filter=filter_chap)
            elif query and not chapter:
                filter_book = Term("book", str(book_num))
                return self._get_results(query, ['chapter_name', 'text'], filter=filter_book)
            elif query and chapter:
                filter_book_chapter = Term("book", str(book_num)) & Term("chapter", str(chapter))
                return self._get_results(query, ['chapter_name', 'text'], filter=filter_book_chapter) 
            else: 
                return self._get_results(book_num, ['book'])

    def query_chapter(self, query: str):
        return self._get_results(query, ['chapter_name'])

    def query_random_book(self):
        int = random.randint(1, 16)
        return self._get_results(int, ['book']) 

    def query_random_line(self):
        int = random.randint(1, 5578)
        return self._get_results(int, ['line'])

    def query_random_chapter(self):
        line = self.query_random_line()['results'][0]
        book = line['book']
        chapter = line['chapter']
        filter_chap = Term("chapter", chapter)
        
        return self._get_results(book, ['book'], filter=filter_chap)

    def return_credits(self):
        return {'credits': self.credits}
