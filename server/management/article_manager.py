from dataclasses import dataclass
from random import random

from server.db.database_manager import DatabaseManager


@dataclass
class Article:
    title: str
    abstract: str
    authors_keywords: str
    keywords_plus: str

class ArticleManager(object):

    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager
        self._num_articles = database_manager.get_number_of_articles()

    def get_random_article(self):
        random_article =  random.randint(1, self._num_articles)
        returned_article_information = self._database_manager.get_article(random_article)
        return Article(returned_article_information[0],
                       returned_article_information[1],
                       returned_article_information[2],
                       returned_article_information[3])




