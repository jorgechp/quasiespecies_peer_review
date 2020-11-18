import os
import re
import csv
import sqlite3

def create_connection(name: str) -> sqlite3.Connection:
    """
    Creates and returns a sqlite connection
    :param name: The name of the databased to which connect.
    :return: A sqlite Connection instance.
    """
    try:
        connection = sqlite3.connect(name)
        return connection
    except sqlite3.Error as e:
        print(e)
        connection.close()
        exit(1)

def translate_quartile_into_impact(quartile: int) -> int:
    if quartile <= 2:
        return 3
    elif quartile == 3:
        return 2
    else:
        return 1

def read_journal_list(path: str, idArea : int, cursorObj : sqlite3.Cursor) -> dict:
    list_of_journals = []
    journal_name_id_dict = dict()

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            journal_name = row["Full Journal Title"]
            journal_impact = row["Journal Impact Factor"]
            list_of_journals.append((journal_name,journal_impact))

    num_of_articles = len(list_of_journals)
    quartile_limit = num_of_articles / 4 + 1

    for index, article in enumerate(list_of_journals):
        current_quartile = int(index / quartile_limit + 1)

        journal_name = article[0].upper()
        journal_impact = article[1]
        journal_impact_type = translate_quartile_into_impact(current_quartile)

        cursorObj.execute(
            """
            INSERT INTO journal(name,quartile,impact,idImpactType,idArea) 
            VALUES
                ('{}',{},{},{},{})            
            """.format(journal_name, current_quartile, journal_impact, journal_impact_type, idArea)
        )
        idJournal = cursorObj.lastrowid
        journal_name_id_dict[journal_name] = idJournal
    csvfile.close()
    return journal_name_id_dict

def read_articles_list(article_csv, cursorObj : sqlite3.Cursor):
    with open(article_csv) as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        for row in reader:
            article_title = s = re.sub(r'[^a-zA-Z0-9 ]', '', row['TI'])
            article_abstract = re.sub(r'[^a-zA-Z0-9 ]', '', row['AB'])
            article_authors_keywords = re.sub(r'[^a-zA-Z0-9 ]', '', row['DE'])
            article_keywords_plus = re.sub(r'[^a-zA-Z0-9 ]', '', row['ID'])
            article_journal = row['SO'].upper()

            if article_journal in general_journal_name_id_dict:
                article_area = general_journal_name_id_dict[article_journal]

                cursorObj.execute(
                    """
                    INSERT INTO article(title,abstract,authors_keywords,keywords_plus,idJournal) 
                    VALUES
                        ('{}','{}','{}','{}',{})            
                    """.format(article_title, article_abstract, article_authors_keywords, article_keywords_plus,article_area)
                )


JOURNAL_LIST = "peer_review/journals/"
ARTICLES_LIST = "peer_review/articles/"

journal_areas = os.listdir(JOURNAL_LIST)
connection = create_connection('instance/peer_review.db')
cursorObj = connection.cursor()

general_journal_name_id_dict = dict()

#Insert Impac types
cursorObj.execute("INSERT INTO impact_type(description) VALUES('LOW')")
cursorObj.execute("INSERT INTO impact_type(description) VALUES('MEDIUM')")
cursorObj.execute("INSERT INTO impact_type(description) VALUES('HIGH')")


#Insert journals
for area in journal_areas:
    area_name = area.replace('_', ' ')

    area_years = os.listdir(JOURNAL_LIST + area)
    for year in area_years:
        year_name = year[:-4]
        cursorObj.execute(
            """
            INSERT INTO area(name,year) 
            VALUES
                ('{}',{})            
            """.format(area_name, year_name)
        )
        idArea = cursorObj.lastrowid
        journal_id_dict = read_journal_list(JOURNAL_LIST + area + '/' + year, idArea, cursorObj)
        general_journal_name_id_dict = {**general_journal_name_id_dict, **journal_id_dict}

#Insert articles

articles_areas = os.listdir(ARTICLES_LIST)

for area in articles_areas:
    articles_folder = ARTICLES_LIST + area
    articles_list = os.listdir(articles_folder)

    for article_csv in articles_list:
        read_articles_list(ARTICLES_LIST + area + '/' + article_csv, cursorObj)

connection.commit()
connection.close()

