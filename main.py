class User:
    def __init__(self, username, password, id) -> None:
        self.username = username
        self.password = password
        self.id = id
        
    def _check_username(self) -> None:
        pass
    
    def _check_password(self) -> None:
        pass


class Note:
    def __init__(self, author) -> None:
        self._check_author(author)
        self.author = author
    
    @classmethod
    def _check_name(cls, name) -> None:
        if type(name) != str:
            raise TypeError("Name, please write string")
        
        if len(name) > 50:
            raise TypeError("Name too long")
    
    @classmethod
    def _check_author(cls, author) -> None:
        test = User('1', '1', 1)
        if type(author) != type(test):
            raise TypeError("Please use User object")
    
    @classmethod
    def _check_text(cls, text) -> None:
        if len(text) > 1000:
            raise TypeError("Text too long")
    
    def create_note(self, name, text) -> None:
        self._check_name(name)
        self._check_text(text)
        
        self.name = name
        self.text = text
    
    def show_note(self):
        print(f"{self.name}\n{self.text}\n{self.author}")


class Book:
    pass

def main() -> None:
    bob = User('Bob', 'super')
    zametka = Note(bob)    
    
    
if __name__ == '__main__':
    main()