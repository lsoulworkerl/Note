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
            
            #data before changes
            start_list = self.get_pickle_data()
            user_data = start_list[0]
            
            #save id user
            user_id = start_list[0][0]
            
            #edit list, delete user login data
            start_list.pop(0)
            note_list.pop(0)
            
            #get id for delete list
            temp_old = []
            temp_new = []
            for i in start_list:
                temp_old.append(i[0])
            
            for i in note_list:
                temp_new.append(i[0])
            
            id_list_delete = list(set(temp_new) ^ set(temp_old))
            
            #delete elements
            for i in id_list_delete:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """DELETE FROM notation WHERE id = '{0}'""".format(i)
                    )
            
            #get id for change
            id_list_change = list(set(temp_new) & set(temp_old))
            
            for i in id_list_delete:
                for l in start_list:
                    if i == l[0]:
                        start_list.remove(l)
                        break
                    
            id_list_change = []
            
            for i in range(0, len(start_list)):
                if start_list[i] != note_list[i]:
                    id_list_change.append(start_list[i][0]) 
            
            #change data
            for i in id_list_change:
                for l in note_list:
                    if i == l[0]:
                        name = l[1]
                        text = l[2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                """UPDATE notation SET name = {0}, 
                                text = {1} WHERE id = '{2}'""".format(name, text, i)
                            )
                    break
            
            #add new data
            for i in note_list:
                if i[0] == -1:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO notation (name, text, id_users) VALUES 
                            (%s, %s, %s)""", (i[1], i[2], user_id)
                        )   
            
            #add user data to list
            note_list.insert(0, user_data)
            
            #edit pickle data
            self.change_pickle_data(note_list)
            
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
    



