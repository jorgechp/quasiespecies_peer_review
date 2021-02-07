
import numpy as np
import itertools
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from db.database_manager import DatabaseManager

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
    total_answers: int

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

    def answer_from_user(self, id_user: int, id_article: int, impact: str, time: int) -> AnswerResult:
        real_journal_impact = self._database_manager.get_impact_type(id_article)

        score = 1 if real_journal_impact == impact else 0

        self._database_manager.add_user_answer(id_user, id_article, impact, score, time)
        number_of_answers = self._database_manager.count_user_score_table(id_user)

        return AnswerResult(real_journal_impact, impact, score, number_of_answers)

    def get_article(self, id_article: int) -> Article:
        returned_article_information = self._database_manager.get_article(id_article)
        return Article(returned_article_information[0],
                       returned_article_information[1],
                       returned_article_information[2],
                       returned_article_information[3].replace(' ', ';'),
                       returned_article_information[4].replace(' ', ';'))

    def get_score(self, user_id: int, partition: int, limit: int) -> UserScores:
        returned_scores = self._database_manager.get_score(user_id, partition, limit)

        positives = sum([row['score'] for row in returned_scores])
        negatives = len(returned_scores) - positives

        return UserScores(user_id,
                          TrainManager.__convert_partition_id_to_impact(partition),
                          positives,
                          negatives)

    def __compute_submission_profile_score(self, user_matrix: np.matrix, partition, submission_profile):
        diagonal = np.diag(user_matrix)
        impact_mask = np.zeros(3)

        for sub_partition, sub_impact in zip(partition, submission_profile):
            for impact_part in sub_partition:
                if impact_part == sub_impact:
                    impact_index = impact_to_index[impact_part]
                    impact_mask[impact_index] = 1

        return np.sum(diagonal * impact_mask)

    def __compute_submission_profile(self, user_matrix_relative_values: np.matrix, partitions_dict: dict, partitions_list: list) -> list:
        submission_profile = dict()
        for partition_index, partition_score in partitions_dict.items():

            partition = partitions_list[partition_index]#
            list_of_profiles = list(itertools.product(list(Impact), repeat=len(partition)))

            max_submission_score = 0
            better_profile = list_of_profiles[0]
            for profile in list_of_profiles:
                submission_score = self.__compute_submission_profile_score(user_matrix_relative_values, partition,profile)
                if submission_score > max_submission_score:
                    max_submission_score = submission_score
                    better_profile = profile

            submission_profile[partition_index] = [p.value for p in better_profile], max_submission_score

        return submission_profile

    def __compute_partition_scores(self, matrix_relative: np.array, partition_list: list) -> dict:
        probabilities_per_impact = dict()
        probabilities_sum = np.sum(matrix_relative, axis=1)

        for impact in Impact:
            index = impact_to_index[impact]
            probabilities_per_impact[impact] = probabilities_sum[index]

        total_probabilities = np.sum(probabilities_sum)

        partition_scores = dict()
        for index_partition, partition in enumerate(partition_list):
            partition_probab = 0
            for sub_partition in partition:
                sub_partition_len = len(sub_partition)
                if sub_partition_len == 1:
                    impact = sub_partition[0]
                    index_impact = impact_to_index[impact]
                    partition_probab += (matrix_relative[index_impact][index_impact]
                                         / probabilities_per_impact[impact]) \
                                       * (probabilities_per_impact[impact]/total_probabilities)
                elif sub_partition_len == 2:
                    for impact_fixed in sub_partition:
                        index_impact_fixed = impact_to_index[impact_fixed]
                        impact_probability = probabilities_per_impact[impact_fixed]
                        partial_prob = impact_probability / total_probabilities
                        for impact_to_compute in sub_partition:
                            if impact_fixed is not impact_to_compute:
                                index_impact_to_compute = impact_to_index[impact_to_compute]
                                partial_prob *= matrix_relative[index_impact_fixed][index_impact_to_compute] \
                                                / impact_probability
                        partition_probab += partial_prob
                else: #Coarse partition
                    pr_li_real_mi_author = matrix_relative[0][1]
                    pr_li_real_hi_author = matrix_relative[0][2]
                    pr_li_real = np.sum(matrix_relative[0])

                    pr_hi_real_li_author = matrix_relative[2][0]
                    pr_hi_real_mi_author = matrix_relative[2][1]
                    pr_hi_real = np.sum(matrix_relative[2])

                    pr_mi_real_mi_author = matrix_relative[1][0]
                    pr_mi_real_hi_author = matrix_relative[1][2]
                    pr_mi_real = np.sum(matrix_relative[1])

                    partition_probab = (pr_li_real_mi_author + pr_li_real_hi_author) * pr_li_real
                    partition_probab += (pr_hi_real_li_author + pr_hi_real_mi_author) * pr_hi_real
                    partition_probab += (pr_mi_real_mi_author + pr_mi_real_hi_author) * pr_mi_real


            partition_scores[index_partition] = partition_probab
        return partition_scores

    def __get_user_partition(self, user_matrix_relative_values: np.array) -> dict:
        scores = dict()

        partition_scores = self.__compute_partition_scores(
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
        user_matrix_relative_column[np.isnan(user_matrix_relative_column)] = 0

        user_stats['score_table'] = score_table
        user_stats['user_partitions'] = self.__get_user_partition( user_matrix_relative_values)

        return user_stats

    def count_user_score_table(self, user_id: str) -> int:
        return self._database_manager.count_user_score_table(user_id)


















