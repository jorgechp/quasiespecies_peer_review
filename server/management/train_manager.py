import itertools

import numpy as np

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from server.db.database_manager import DatabaseManager


class Impact(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


PARTITIONS = [
    [[Impact.LOW, Impact.MEDIUM], [Impact.HIGH]],
    [[Impact.LOW, Impact.HIGH], [Impact.MEDIUM]],
    [[Impact.MEDIUM, Impact.HIGH], [Impact.LOW]],
    [[Impact.LOW, Impact.MEDIUM, Impact.HIGH]],
    [[Impact.LOW], [Impact.MEDIUM], [Impact.HIGH]],
]


impact_to_index = dict()
impact_to_index[Impact.LOW] = 0
impact_to_index[Impact.MEDIUM] = 1
impact_to_index[Impact.HIGH] = 2

index_to_impact = {v: k for k, v in impact_to_index.items()}


def partition_to_str(partition: list) -> str:
    partition_str = []
    for sub_partiton in partition:
        partition_str.append([impact.value for impact in sub_partiton])
    return partition_str


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

    def __compute_submission_profile(self, user_matrix_relative_values: np.matrix, partitions_dict: dict, partitions_list: list) -> list:
        submission_profile = dict()
        for partition_index, partition_score in partitions_dict.items():

            partition = partitions_list[partition_index]
            sub_partition_score = []
            for sub_partition in partition:
                if len(sub_partition) == 1:
                    index = impact_to_index[sub_partition[0]]
                    roi_matrix = user_matrix_relative_values[index].reshape((1,3))
                else:
                    quality_indices = [impact_to_index[impact] for impact in sub_partition]
                    roi_matrix = user_matrix_relative_values[quality_indices]

                profile_impact_dict = dict()
                for impact_type in Impact:
                    impact_index = impact_to_index[impact_type]
                    profile_score = np.sum(roi_matrix[:, impact_index]) * partition_score
                    profile_impact_dict[impact_type.value] = profile_score

                profile_impact_dict = {k: v for k, v in sorted(profile_impact_dict.items(),
                                         key=lambda item: item[1],
                                         reverse=True)}
                sub_partition_score.append(profile_impact_dict)
            submission_profile[partition_index] = sub_partition_score

        return submission_profile

    def __compute_partition_scores(self, matrix_relative_quality: np.array, matrix_relative: np.array, partition_list: list) -> dict:
        probabilities_per_impact = dict()
        probabilities_sum = np.sum(matrix_relative, axis=1)

        for impact in Impact:
            index = impact_to_index[impact]
            probabilities_per_impact[impact] = probabilities_sum[index]

        partition_scores = dict()
        for index_partition, partition in enumerate(partition_list):
            partition_score = 0
            for sub_partition in partition:
                if len(sub_partition) == 1:
                    impact = sub_partition[0]
                    index_impact = impact_to_index[impact]
                    partition_score += matrix_relative_quality[index_impact][index_impact] \
                                       * probabilities_per_impact[impact]
                else:
                    impacts_to_preserve = set([impact_to_index[impact] for impact in sub_partition])
                    for quality in sub_partition:
                        index_quality = impact_to_index[quality]
                        impacts_to_preserve_fixed_quality = list(impacts_to_preserve - {index_quality})
                        matrix_roi = matrix_relative_quality[:,impacts_to_preserve_fixed_quality]
                        partition_score += np.prod(matrix_roi[index_quality]) * probabilities_per_impact[quality]
            partition_scores[index_partition] = partition_score
        return partition_scores

    def __get_user_partition(self, user_matrix_relative_column: np.array, user_matrix_relative_values: np.array) -> dict:
        scores = dict()

        partition_scores = self.__compute_partition_scores(
            user_matrix_relative_column,
            user_matrix_relative_values,
            PARTITIONS)

        partition_scores = {int(k): v for k, v in sorted(partition_scores.items(),
                                                         key=lambda item: item[1],
                                                         reverse=True)}
        scores['partitions'] = partition_scores
        submission_profiles = self.__compute_submission_profile(user_matrix_relative_values, partition_scores, PARTITIONS)
        scores['submissions'] = submission_profiles
        scores['partitions_keys'] = [partition_to_str(partition) for partition in PARTITIONS]
        return scores



    def get_user_score_table(self, user_id: str, first = -1) -> dict:
        impact_list = [e.value for e in Impact]

        user_stats = dict()
        score_table = dict()

        for target_impact in impact_list:
            current_score_table = dict()
            for user_impact in impact_list:
                number_of_occurrences = self._database_manager.get_user_score_table(user_id,
                                                                  first,
                                                                  target_impact,
                                                                  user_impact )
                current_score_table[user_impact] = number_of_occurrences
                score_table[target_impact] = current_score_table

        user_matrix_full_values = np.zeros((3, 3))
        user_matrix_full_values[0][0] = score_table['LOW']['LOW']
        user_matrix_full_values[0][1] = score_table['LOW']['MEDIUM']
        user_matrix_full_values[0][2] = score_table['LOW']['HIGH']
        user_matrix_full_values[1][0] = score_table['MEDIUM']['LOW']
        user_matrix_full_values[1][1] = score_table['MEDIUM']['MEDIUM']
        user_matrix_full_values[1][2] = score_table['MEDIUM']['HIGH']
        user_matrix_full_values[2][0] = score_table['HIGH']['LOW']
        user_matrix_full_values[2][1] = score_table['HIGH']['MEDIUM']
        user_matrix_full_values[2][2] = score_table['HIGH']['HIGH']

        user_matrix_relative_values = user_matrix_full_values / np.sum(user_matrix_full_values)
        user_matrix_relative_column = user_matrix_full_values / user_matrix_full_values.sum(axis=1, keepdims=True)

        user_stats['score_table'] = score_table
        user_stats['user_partitions'] = self.__get_user_partition(user_matrix_relative_column, user_matrix_relative_values)

        return user_stats

    def count_user_score_table(self, user_id: str) -> int:
        return self._database_manager.count_user_score_table(user_id)


















