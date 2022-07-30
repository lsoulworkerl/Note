from database import Data
from note import User, Note


class Work:
    def __init__(self, profile: User, db: Data) -> None:
        self.profile = profile
        self.db = db
        
    def _main_interface(self) -> list:
        self.db.get_db_data(self.profile.id)
        user_note = self.db.get_pickle_data()
        return user_note
    
    def new_note(self, note: Note) -> list:
        user_note = self._main_interface()
        new_note = [-1, note.name, note.text]
        user_note.append(new_note)
        return user_note
    
    def edit_note(self, note: Note, id_note) -> list:
        user_note = self._main_interface()
        edit = 1
        for i in user_note[1:]:
            if edit == id_note:
                user_note[edit][1] = note.name
                user_note[edit][2] = note.text
                break             
            edit += 1
        
        return user_note
                
    def delete_note(self, id_delete) -> list:
        user_note = self._main_interface()
        delete = 1
        for i in user_note[1:]:
            if delete == id_delete:
                user_note.pop(delete)
                break
            delete += 1
            
        return user_note
    
    def get_note(self):
        temp = self._main_interface()
        return temp
    
    def end_work(self, user_note):
        self.db.change_db_data(user_note)
        self.db.change_pickle_data(user_note)
        