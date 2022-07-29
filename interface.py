from note import User, Note


class Interface():
    def __init__(self) -> None:
        pass
    
    def registration(self, username_db) -> User:
        username = input("Please write username\n")
        
        for i in username_db:
            if i[0] == username:
                raise TypeError("Please use another username")
            
        password = input("Please write password\n")      
        profile = User(username, password)
        
        return profile
    
    def authorisation(self, username_db) -> User:
        username = input("Please write username\n")
        for i in username_db:
            if i[0] == username:
                password = input("Please write password\n")
                if password == i[1]:
                    profile = User(i[0], i[1], int(i[2]))
                    return profile
                else:
                    raise TypeError("Wrong password")
        else:
            raise TypeError("Please register")


def main() -> None:
    '''dict_user = {'test': 'test'}
    test = Interface()
    
    i = int(input("1 - authorisation \n2 - registration \n"))
    if i == 1:
        profile = test.authorisation(dict_user)
        
    elif i == 2:
        profile = test.registration(dict_user)

    test_note = Note(profile)
    name = input("Please write name\n")
    text = input("Please write text\n")
    test_note.create_note(name, text)
    test_note.show_note()'''
    test = Interface()
    profile = test.registration()
    
if __name__ == '__main__':
    main()
    #usernames = database.get_username()
    #print(usernames[0][0])