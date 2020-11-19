from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from typing import List

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

@dataclass_json
@dataclass
class UserScores:
    user_id: int
    partition_type: Impact
    positive_score: int
    negative_score: int

@dataclass_json
@dataclass
class ScorePerImpact:
    answer_impact: Impact
    occurrences: int

@dataclass_json
@dataclass
class ScoreTable:
    target_impact: Impact
    scores: List[ScorePerImpact]


class TrainManager(object):

    @staticmethod
    def __convert_partition_id_to_impact(partition: int) -> str:
        if partition == 1:
            return "LOW"
        elif partition == 2:
            return "MEDIUM"
        elif partition == 3:
            return "HIGH"
        else:
            return 0

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

    def get_quartile_score(self, user_id: int, partition: int, limit: int) -> UserScores:
        returned_scores = self._database_manager.get_quartile_score(user_id, partition, limit)

        positives = sum([row['score'] for row in returned_scores])
        negatives = len(returned_scores) - positives

        return UserScores(user_id,
                          TrainManager.__convert_partition_id_to_impact(partition),
                          positives,
                          negatives)

    def get_user_score_table(self, user_id: str, limit: int) -> dict:
        impact_list = list(map(str, Impact))

        score_per_impact_dict = dict()

        for target_impact in impact_list:
            current_score_table = dict()
            for user_impact in impact_list:
                target_impact_preprocessed = target_impact.split('.')[1]
                user_impact_preprocessed = user_impact.split('.')[1]

                number_of_occurrences = self._database_manager.get_user_score_table(user_id,
                                                                  limit,
                                                                  target_impact_preprocessed,
                                                                  user_impact_preprocessed )
                current_score_table[user_impact] = number_of_occurrences
                score_per_impact_dict[target_impact] = current_score_table
        return score_per_impact_dict















