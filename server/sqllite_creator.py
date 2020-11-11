import sqlite3

"""
THIS SCRIPT CREATES THE JOURNALS AND THE USERS DATABASE. 
"""

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


connection_journals = create_connection('articles.db')

#CREATING JOURNALS AND ARTICLES

try:
    cursorObj = connection_journals.cursor()

    cursorObj.execute(
        """
            CREATE TABLE area(
                        idArea INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        year INTEGER NOT NULL   
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE journal(
                        idJournal INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        quartile INTEGER NOT NULL,
                        impact INTEGER NOT NULL,
                        idArea INTEGER NOT NULL,
                        
                        FOREIGN KEY(idArea) REFERENCES area(idArea)
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE article(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        title TEXT NOT NULL, 
                        abstract TEXT NOT NULL, 
                        authors_keywords TEXT,
                        keywords_plus TEXT,
                        idJournal INTEGER,
                        
                        FOREIGN KEY(idJournal) REFERENCES journal(idJournal)
                )
        """
    )
    connection_journals.commit()
    connection_journals.close()
except sqlite3.Error as er:
    print(er)


connection_users = create_connection('users.db')

# CREATING USERS
try:
    cursorObj = connection_users.cursor()
    cursorObj.execute(
        """
            CREATE TABLE user(
                        idUser INTEGER PRIMARY KEY AUTOINCREMENT,
                        mail TEXT NOT NULL                        
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE submission_response(
                        idSubmissionResponse TEXT PRIMARY KEY                                              
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE article_type(
                        idArticleType TEXT PRIMARY KEY                                              
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE partition(
                        idPartition INTEGER PRIMARY KEY                                              
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE user_partitions(
                        idUser INTEGER NOT NULL,
                        idArticleType TEXT NOT NULL,
                        idPartition INTEGER NOT NULL,
                        
                        PRIMARY KEY(idUser, idArticleType),
                        
                        FOREIGN KEY(idUser) REFERENCES user(idUser),
                        FOREIGN KEY(idArticleType) REFERENCES article_type(idArticleType),       
                        FOREIGN KEY(idPartition) REFERENCES partition(idPartition)                                          
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE submission_profile(
                        idUser INTEGER NOT NULL,                        
                        idPartition INTEGER NOT NULL,
                        idSubmissionResponse TEXT NOT NULL,

                        PRIMARY KEY(idUser, idPartition, idSubmissionResponse),

                        FOREIGN KEY(idUser) REFERENCES user(idUser),
                        FOREIGN KEY(idPartition) REFERENCES partition(idPartition),       
                        FOREIGN KEY(idSubmissionResponse) REFERENCES submission_response(idSubmissionResponse)                                          
                )
        """
    )


    connection_users.commit()
    connection_users.close()
except sqlite3.Error as er:
    print(er)