from config import host, user, password, db_name
from database import Data
from interface import Interface
from note import User, Note
from console_interface import Work

def workspace(space: Work) -> None:
    while True:
        temp_note = Note(space.profile)
        user_note = space.get_note()
        
        user_note.pop(0)
        choice = int(input("1 - show note\n2 - new note\n3 - edit note\n4 - delete note\n5 - end of work\n"))
        
        #show note
        if choice == 1:
            print(user_note)
        
        #create new note
        if choice == 2:
            name = input("Please write name\n")
            text = input("Please write text\n")
            temp_note.create_note(name, text)
            user_note = space.new_note(temp_note)
        
        #edit note
        if choice == 3:
            print(user_note)
            #choose what note to edit
            edit = int(input("What do you want to edit?\n"))
            #edit name
            change = int(input("Do you want to change name?\n1 - yes\n2- not\n"))
            if change == 1:
                name = input("Please write new name\n")
            if change == 2:
                name = user_note[edit][1]
            #edit text
            change = int(input("Do you want to change text?\n1 - yes\n2- not\n"))
            if change == 1:
                text = input("Please write new name\n")
            if change == 2:
                text = user_note[edit][2]
            temp_note.create_note(name, text)
            user_note = space.edit_note(temp_note, edit)
            print(user_note)
        
        #delete note
        if choice == 4:
            pass
        
        if choice == 5:
            space.end_work(user_note)
            break
        
        
def main() -> None:
    db = Data(host, user, password, db_name)
    interface = Interface()
    login = int(input("1 - authorisation\n2 - registration\n3 - exit\n"))
    user_information = db.get_db_user()
    
    if login == 1:
        login_user = interface.authorisation(user_information)
        space = Work(login_user, db)
        workspace(space)
        
    if login == 2:
        new_user = interface.registration(user_information)
        db.add_new_user(new_user)
        space = Work(new_user, db)
        workspace(space)
        
    if login == 3:
        pass

if __name__ == '__main__':
    main()
