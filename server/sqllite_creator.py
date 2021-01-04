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


connection = create_connection('./instance/peer_review.db')


try:
    cursorObj = connection.cursor()

    cursorObj.execute(
        """
            CREATE TABLE area(
                        idArea INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        year INTEGER NOT NULL   
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE journal(
                        idJournal INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        quartile INTEGER NOT NULL,
                        impact INTEGER NOT NULL,                      
                        idImpactType INTEGER NOT NULL,
                        idArea INTEGER NOT NULL,
                        
                        FOREIGN KEY(idArea) REFERENCES area(idArea) ON DELETE CASCADE,
                        FOREIGN KEY(idImpactType) REFERENCES impact_type(idImpactType) ON DELETE CASCADE   
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE article(
                        idArticle INTEGER PRIMARY KEY, 
                        title TEXT NOT NULL, 
                        abstract TEXT NOT NULL, 
                        authors_keywords TEXT,
                        keywords_plus TEXT,
                        idJournal INTEGER,
                        
                        FOREIGN KEY(idJournal) REFERENCES journal(idJournal) ON DELETE CASCADE
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE role(
                        idRole INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL                     
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE user(
                        idUser INTEGER PRIMARY KEY,
                        nick TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        mail TEXT NOT NULL,
                        language TEXT DEFAULT 'en'                     
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE user_has_role(
                        idUser INTEGER NOT NULL,
                        idRole INTEGER NOT NULL,
                        
                        PRIMARY KEY(idUser,idRole),
                        FOREIGN KEY(idUser) REFERENCES user(idUser) ON DELETE CASCADE,              
                        FOREIGN KEY(idRole) REFERENCES role(idRole) ON DELETE CASCADE             
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE user_answer_article(
                        idAnswer INTEGER PRIMARY KEY,
                        idUser INTEGER NOT NULL,
                        idArticle INTEGER NOT NULL,
                        date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        userAnswerImpact INTEGER NOT NULL, 
                        realImpact INTEGER NOT NULL,            
                        score INTEGER NOT NULL,                       
                        
                        
                        FOREIGN KEY(idUser) REFERENCES user(idUser) ON DELETE CASCADE,
                        FOREIGN KEY(idArticle) REFERENCES article(idArticle) ON DELETE CASCADE,
                        FOREIGN KEY(userAnswerImpact) REFERENCES impact_type(idImpactType) ON DELETE CASCADE,
                        FOREIGN KEY(realImpact) REFERENCES impact_type(idImpactType) ON DELETE CASCADE
                                                               
                )
        """
    )


    cursorObj.execute(
        """
            CREATE TABLE impact_type(
                        idImpactType INTEGER PRIMARY KEY,
                        description TEXT UNIQUE NOT NULL                                      
                )
        """
    )

    cursorObj.execute(
        """
            CREATE TABLE user_tokens(
                        idUser INTEGER PRIMARY KEY,
                        client_token TEXT UNIQUE NOT NULL,     
                        cookie_token TEXT UNIQUE NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        
                        FOREIGN KEY(idUser) REFERENCES user(idUser) ON DELETE CASCADE                                  
                )
        """
    )

    connection.commit()
    connection.close()
except sqlite3.Error as er:
    print(er)