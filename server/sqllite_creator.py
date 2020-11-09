import sqlite3


def create_connection(name: str) -> None:
    try:
        connection = sqlite3.connect(name)
        return connection
    except e:
        print(e)
        connection.close()
        exit(1)


connection_articles = create_connection('articles.db')
connection_users = create_connection('users.db')

#CREATING JOURNALS

try:
    cursorObj = connection_articles.cursor()
    cursorObj.execute(
        """
            CREATE TABLE journal(
                        idJournal INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        quartile INTEGER NOT NULL
                )
        """
    )
    cursorObj.execute(
        """
            CREATE TABLE article(
                        id INTEGER PRIMARY KEY, 
                        title TEXT NOT NULL, 
                        abstract TEXT NOT NULL, 
                        keywords TEXT,
                        idJournal INTEGER,
                        
                        FOREIGN KEY(idJournal) REFERENCES journal(idJournal)
                )
        """
    )
    connection_articles.commit()
except sqlite3.Error as er:
    print(er)