import numpy as np

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from server.db.database_manager import DatabaseManager


class Impact(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


PARTITIONS = set()
PARTITIONS.add(((Impact.LOW), (Impact.MEDIUM), (Impact.HIGH)))
PARTITIONS.add(((Impact.LOW, Impact.MEDIUM), (Impact.HIGH)))
PARTITIONS.add(((Impact.LOW, Impact.HIGH), (Impact.MEDIUM)))
PARTITIONS.add(((Impact.MEDIUM, Impact.HIGH), (Impact.LOW)))
PARTITIONS.add(((Impact.LOW, Impact.MEDIUM, Impact.HIGH)))

partition_to_index = dict()
partition_to_index[Impact.LOW.value] = 0
partition_to_index[Impact.MEDIUM.value] = 1
partition_to_index[Impact.HIGH.value] = 2


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
    real_journal_quality: str
    user_journal_quality: str
    user_score: int

@dataclass_json
@dataclass
class UserScores:
    user_id: int
    partition_type: Impact
    positive_score: int
    negative_score: int

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

    @staticmethod
    def __parse_impact(impact):
        if impact == 'LOW':
            return Impact.LOW
        elif impact == 'MEDIUM':
            return Impact.MEDIUM
        else:
            return Impact.HIGH

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

    def answer_from_user(self, id_user: int, id_article: int, impact: str) -> AnswerResult:
        real_quartile = self._database_manager.get_quartile_from_article(id_article)
        real_journal_impact = TrainManager.__convert_quartile_to_impact(real_quartile)
        user_journal_impact = TrainManager.__parse_impact(impact)
        score = 1 if real_journal_impact is user_journal_impact else 0

        self._database_manager.add_user_answer(id_user, id_article, impact, score)

        return AnswerResult(real_journal_impact.value, user_journal_impact.value, score)

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

    def __get_user_partition(self, score_per_impact: dict):
        scores = []
        user_matrix_full_values = np.zeros((3, 3))
        user_matrix_full_values[0][0] = score_per_impact['LOW']['LOW']
        user_matrix_full_values[0][1] = score_per_impact['LOW']['MEDIUM']
        user_matrix_full_values[0][2] = score_per_impact['LOW']['HIGH']
        user_matrix_full_values[1][0] = score_per_impact['MEDIUM']['LOW']
        user_matrix_full_values[1][1] = score_per_impact['MEDIUM']['MEDIUM']
        user_matrix_full_values[1][2] = score_per_impact['MEDIUM']['HIGH']
        user_matrix_full_values[2][0] = score_per_impact['HIGH']['LOW']
        user_matrix_full_values[2][1] = score_per_impact['HIGH']['MEDIUM']
        user_matrix_full_values[2][2] = score_per_impact['HIGH']['HIGH']

        user_matrix_relative_values = user_matrix_full_values / np.sum(user_matrix_full_values)
        user_matrix_relative_column = user_matrix_full_values / user_matrix_full_values.sum(axis=1, keepdims=True)


        for partition in PARTITIONS:
            sub_partition_score = 0
            for sub_partition in partition:
                quality_max_score = 0
                for quality in sub_partition:
                    article_quality_index = partition_to_index[quality.value]
                    s = 0
                    for impact in sub_partition:
                        impact_quality_index = partition_to_index[impact.value]
                        s += user_matrix_relative_column[article_quality_index][impact_quality_index], quality_max_score

                sub_partition_score += quality_max_score

            scores.append(sub_partition_score)
        return sum(scores)

    def get_user_score_table(self, user_id: str, limit: int) -> dict:
        impact_list = [e.value for e in Impact]

        score_per_impact_dict = dict()

        for target_impact in impact_list:
            current_score_table = dict()
            for user_impact in impact_list:
                number_of_occurrences = self._database_manager.get_user_score_table(user_id,
                                                                  limit,
                                                                  target_impact,
                                                                  user_impact )
                current_score_table[user_impact] = number_of_occurrences
                score_per_impact_dict[target_impact] = current_score_table

        user_partition = self.__get_user_partition(score_per_impact_dict)

        return score_per_impact_dict
















