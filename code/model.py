class User:
    id: int = None
    login: str
    password: str
    is_online: bool = False
    rating = 0
    role: int  # 1- seller, 2- buyer, 3- admin

    def __str__(self):
        return f"User id: {self.id}, login: {self.login}, password_hash: {self.password}," \
               f"The is online: {self.is_online}, user's rating: {self.rating}, user's role: {self.role} "


class Album:
    id: int
    title: str = None
    artist: str = None
    release_year: int = None
    genre: str = None

    def __str__(self):
        return f"Album id: {self.id}, title {self.title}, artist: {self.artist}," \
               f" release year {self.release_year}, genre: {self.genre}"


class Edition:
    id: int
    year: int = None
    label_id: int = None
    is_remastered: bool = None
    label: str = None
    price: int = None

    def __str__(self):
        return f"Edition id: {self.id}, edition year {self.year}," \
               f"label id {self.label_id}, is it remastered {self.is_remastered}, price: {self.price}"


"""

class Item:
    id: int
    user_id: int
    edition_id: int = None
    create_date: datetime.datetime = None
    price: int = None

    def __str__(self):
        return f"Item's ID: {self.id}, creator's ID {self.user_id}, edition ID {self.edition_id},creation date "\
                 "{self.create_date}, price: {self.price}"
                 
class Artist:
    id: int
    name: str

    def __str__(self):
        return f"Artist id {self.id}, name: {self.name}"


class Label:
    id: int
    name: str

    def __str__(self):
        return f"Label id {self.id}, name: {self.name}"



class UserRole:
    id: int
    role_name: str

    def __str__(self):
        return f"Role id: {self.id}, role name: {self.role_name}"


class UsersRoles(UserList, UserRole):
    UserRole.id: int
    UserList.id: int

    def __str__(self):
        return f"User ID is {UserList.id}, user role is {UserRole.id}"
"""
