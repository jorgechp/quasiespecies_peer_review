import sqlite3
from collections import Counter
from typing import List
from operator import itemgetter

from db.database_manager import DatabaseManager
from management.train_manager import TrainManager, PARTITIONS
from management.user_manager import UserManager

conn = sqlite3.connect('../instance/peer_review.db')
database_manager: DatabaseManager = DatabaseManager(database_connection=conn)
user_manager: UserManager = UserManager(database_manager, '../security/key')
train_manager: TrainManager = TrainManager(database_manager)

#Get all users nicks
nicks_response: List[tuple] = user_manager.get_users_nicknames()

good_users = 0
bad_users = 0
f_results = open("results.txt", "w")
f_good = open("good_users.txt", "w")
f_bad = open("bad_users.txt", "w")


def convert_keys_to_values(max_partitions_dict):
    return PARTITIONS[max_partitions_dict]


list_partitions = []
list_submission_profiles = []

for nick in nicks_response:
    user_id: str = str(user_manager.get_user_id(nick[0]))
    # user_id: str = str(user_manager.get_user_id("FranRodrigo"))

    score_tables = []
    rows_per_step = 30
    number_of_results = train_manager.count_user_score_table(user_id)

    if number_of_results > 14:
        good_users = good_users + 1
        rows_per_step = rows_per_step if rows_per_step < number_of_results else number_of_results
        number_of_steps = int(number_of_results / rows_per_step) + 1
        for step in range(1, number_of_steps):
            number_of_rows = rows_per_step * step
            score_tables.append(train_manager.get_user_score_table(user_id, first=number_of_rows))
        print(nick)
        partitions_dict = score_tables[0]['user_partitions']['partitions']
        max_partitions_dict = max(partitions_dict.items(), key=itemgetter(1, 0))[0]

        partition_str = str(PARTITIONS[max_partitions_dict])

        submissions_dict = score_tables[0]['user_partitions']['submissions']
        submission_profile = submissions_dict[max_partitions_dict][0]
        submission_str = str(submission_profile)


        f_results.write("{};{}\n".format(partition_str, submission_str))
        f_good.write("{} has {} results\n".format(nick,number_of_results))

        list_partitions.append(partition_str)
        list_submission_profiles.append(str(submission_str))

    else:
        bad_users = bad_users + 1
        f_bad.write("{} has {} results\n".format(nick,number_of_results))

distinct_list_partitions = Counter(list_partitions)
distinct_list_submission_profiles = Counter(list_submission_profiles)
f_results.close()
f_good.close()
f_bad.close()
print("Good users: {} - Bad users {}".format(good_users, bad_users))



