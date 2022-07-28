import psycopg2
from config import host, user, password, db_name
from interface import Interface
from main import User, Note

try:
    connection = psycopg2.connect(
        host = host,
        user = user,
        password = password,
        database = db_name
        )
    connection.autocommit = True
    #create interface
    test = Interface()
    
    #get data from a table
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT username, password, id FROM users"""
        )
        usernames_db = cursor.fetchall()
    while True:
        i = int(input('What do u want?'))
        #test
        if i == 0:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT username FROM users WHERE id = 2"""
                )
                testing = cursor.fetchall()
            print(testing)
        if i == 1:
            #registration
            profile = test.registration(usernames_db)
            with connection.cursor() as cursor:
                cursor.execute(
                        """INSERT INTO users (username, password) VALUES
                        (%s, %s)""", (profile.username, profile.password)
                    )
        if i == 2:
            #authorisation
            profile = test.authorisation(usernames_db)
            event = int(input('What do u want'))
            #create note
            if event == 1:
                creation = Note(profile)
                name = input('Please write name of your notation')
                text = input('Please write the text of your notation')
                creation.create_note(name, text)
                with connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO notation (name, text, id_users) VALUES
                        (%s, %s, %s)""", (creation.name, creation.text, profile.id)
                    )
                break
            #show note
            if event == 2:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT (name, text) FROM notation WHERE
                        id_users = %s""", str(profile.id)
                    )
                    note = cursor.fetchall()
                print(note)
            #delete note
            if event == 3:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT name, text FROM notation WHERE
                        id_users = %s""", str(profile.id)
                    )
                    note = cursor.fetchall()
                print(note)
                number = 1
                for i in note:
                    print(number)
                    number += 1
                    print(i[0])
                    print(i[1])
                number = int(input('What do u want to delete? Pls, wirte number'))
                z = 1
                for i in note:
                    if number == z:
                        delete_name = i[0]
                        print(delete_name)
                    z += 1
                with connection.cursor() as cursor:
                    cursor.execute(
                        """DELETE FROM notation WHERE name = '{0}'""".format(delete_name) 
                    )
        if i == 3:
            #exit account
            break
    
except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
            connection.close()
            print("End of work database")



