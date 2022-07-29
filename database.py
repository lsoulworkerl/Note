import psycopg2
import pickle


class Data:
    def __init__(self, host, user, password, db_name) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
    
    #get user note from db
    def get_db_data(self, id_user) -> None: 
        try:
            
            #login in db
            connection = psycopg2.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.db_name
            )
            connection.autocommit = True
            
            #get user note
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT id, name, text FROM notation WHERE id_users = '{0}'""".format(id_user)
                )
                note = cursor.fetchall()
                
            #get author name
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT username, password FROM users WHERE id = '{0}'""".format(id_user)
                )
                author = cursor.fetchall()
                author = list(author[0])
                author = author.insert(0, id_user)

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            #end of work with db
            if connection:
                connection.close()
                
        #change tuple in list
        note_list = []
        for i in note:
            note_list.append(list(i))

        #[0] - id of user, his username and password
        note_list.insert(0, author)
        
        #create pickle file
        export_note = open('database.pickle','wb')
        pickle.dump(note_list, export_note)
        export_note.close()
    
    #after user work accept changes
    def change_db_data(self, note_list) -> None:
        try:
            
            #login in db
            connection = psycopg2.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.db_name
            )
            connection.autocommit = True
            
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            #end of work with db
            if connection:
                connection.close()
    
    #change pickle data
    def change_pickle_data(self, note_list) -> None:
        export_note = open('database.pickle','wb')
        pickle.dump(note_list, export_note)
        export_note.close()
    
    #get pickle list data
    def get_pickle_data(self) -> list:
        import_note = open('database.pickle', 'rb')
        note_list = pickle.load(import_note)
        return note_list
    



