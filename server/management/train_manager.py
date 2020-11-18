from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

from server.db.database_manager import DatabaseManager

@dataclass_json
class Impact(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@dataclass_json
@dataclass
class Article:
    id: int
    title: str
    abstract: str
    authors_keywords: str
    keywords_plus: str

@dataclass_json
@dataclass
class AnswerResult:
    user_id_journal: int
    real_journal_quality: Impact
    user_journal_quality: Impact
    user_score: int


class TrainManager(object):

    @staticmethod
    def __convert_quartile_to_impact(quartile: int) -> Impact:
        if quartile <= 2:
            return Impact.HIGH
        elif quartile == 3:
            return Impact.MEDIUM
        else:
            return Impact.LOW

    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager
        self._num_articles = database_manager.get_number_of_articles()

    def get_random_article(self) -> Article:
        returned_article_information = self._database_manager.get_random_article()
        return Article(returned_article_information[0],
                       returned_article_information[1],
                       returned_article_information[2],
                       returned_article_information[3].replace(' ', ';'),
                       returned_article_information[4].replace(' ', ';'))

    def get_quartile_of_journal(self, article_to_check : Article) -> int:
        return self._database_manager.get_quartile_from_article(article_to_check.id)

    def answer_from_user(self, id_user: int, id_article: int, quartile: int) -> AnswerResult:
        real_quartile = self._database_manager.get_quartile_from_article(id_article)
        real_journal_quality = TrainManager.__convert_quartile_to_impact(real_quartile)
        user_journal_quality = TrainManager.__convert_quartile_to_impact(quartile)
        score = 1 if real_journal_quality == user_journal_quality else 0

        self._database_manager.add_user_answer(id_user, id_article, quartile, score)

        return AnswerResult(quartile, real_journal_quality, user_journal_quality, score)

    def get_article(self, id_article: int) -> Article:
        returned_article_information = self._database_manager.get_article(id_article)
        return Article(returned_article_information[0],
                       returned_article_information[1],
                       returned_article_information[2],
                       returned_article_information[3].replace(' ', ';'),
                       returned_article_information[4].replace(' ', ';'))








