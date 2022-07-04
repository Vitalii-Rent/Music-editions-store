# import model
from model import *
from database import *
from tabulate import tabulate
from typing import List, Tuple, Any


class Interface:
    def __init__(self):
        self.db = DataBase()
        self.user = User()

    @staticmethod
    def ans_int(prompt: str = " "):
        while True:
            try:
                ans = float(input(prompt))
                return ans
            except TypeError and ValueError:
                print("Incorrect data type input ")

    def update_item(self):
        print("List of your current items: ")
        items, err = self.db.select_all_items(self.user.id)
        if self.print_item(items) == 1:
            return
        while True:
            try:
                item_id = ans = self.ans_int("Enter the number of item you want to update ")
                res, item, err = self.db.select_one_item(ans)  # item - tuple(0 - Album, 1 - Edition
                l = [list(res.values())]
                h = list(res.keys())
                break
            except (AttributeError, ValueError, TypeError):  # and ValueError and TypeError
                print("Incorrect data type input(probably wrong number) ")
        # self.print_item(res)
        print(tabulate(l, h, tablefmt="pretty"))
        # old_item = self.db.select_one_item(ans)
        print("That was an old version")
        print("Firstly, enter the title and the artist's name ")
        ans = input("Enter the album's title(if you want to save old - enter 1) : ").title()
        if ans != "1": item[0].title = ans
        ans = input("Enter the album's artist(if you want to save old - enter 1) : ").title()
        if ans != "1": item[0].artist = ans
        ans = self.ans_int("Enter the album's release year(if you want to save old - enter 1) : ")
        if ans != 1: item[0].release_year = ans
        ans = input("Enter the album's genre(if you want to save old - enter 1) : ").title()
        if ans != "1": item[0].genre = ans
        print("Then, let's specify the exact edition you want to sell or buy ")
        ans = input("Enter the edition's label(if you want to save old - enter 1) : ").title()
        if ans != "1": item[1].label = ans
        ans = self.ans_int("Enter the edition's year(if you want to save old - enter 1) : ")
        if ans != 1: item[1].year = ans
        ans = self.ans_int("Enter the edition's price(if you want to save old - enter 1) : ")
        if ans != 1: item[1].price = ans

        while True:
            if self.user.role == 1:
                ans = input("Is your edition remastered? (y - yes, n - no) ")
            else:
                ans = input("Do you want your edition to be remastered (y - yes, n - no) ")
            match ans:
                case "y":
                    item[1].is_remastered = True
                    break
                case "n":
                    item[1].is_remastered = False
                    break
                case _:
                    print("Your input is incorrect, don't worry, you can update info later on ")

        if self.user.role == 1:
            it_type = 'offer'
        elif self.user.role == 2:
            it_type = 'request'
        else:
            print("Unknown error")
            return
        result, err = self.db.update_item(item, item_id, it_type, self.user.id)
        l = [list(result.values())]
        h = list(result.keys())
        print(tabulate(l, h, tablefmt="pretty"))

    def create_item(self):
        # item = model.Item()
        album = Album()
        edition = Edition()
        x = input("Quick?(1) ")
        if x == "1":
            album.title = "Let It Be"
            album.artist = "The Beatles"
            album.release_year = 1970
            album.genre = "rock"
            edition.label = "EMI"
            edition.year = 1985
            edition.price = 500
            edition.is_remastered = False
            if self.user.role == 1:
                type = 'offer'
            else:
                type = 'request'
            self.db.insert_item(type, self.user.id, album, edition)
            print("Insertion is correct! ")
            return

        print("Firstly, enter the title and the artist's name ")
        album.title = input("Enter the album's title: ").title()
        album.artist = input("Enter the album's artist: ").title()
        album.release_year = self.ans_int("Enter the album's release year ")
        album.genre = input("Enter the album's genre ").title()
        print("Then, let's specify the exact edition you want to sell or buy ")
        edition.label = input("Enter the edition's label: ").title()
        edition.year = self.ans_int("Enter the edition's release year: ")
        edition.price = self.ans_int("Enter the item's price: ")

        while True:
            if self.user.role == 1:
                ans = input("Is your edition remastered? (y - yes, n - no) ")
            else:
                ans = input("Do you want your edition to be remastered (y - yes, n - no) ")
            match ans:
                case "y":
                    edition.is_remastered = True
                    break
                case "n":
                    edition.is_remastered = False
                    break
                case _:
                    print("Your input is incorrect, don't worry, you can update info later on ")

        if self.user.role == 1:
            type = 'offer'
        else:
            type = 'request'
        result, err = self.db.insert_item(type, self.user.id, album, edition)
        if not result:
            print("Something went wrong ")
            return
        print("Your item! ")
        l = [list(result.values())]
        h = list(result.keys())
        print(tabulate(l, h, tablefmt="pretty"))
        # self.user_menu()

    @staticmethod
    def separate_headers_and_items(select_result: List[dict]) -> Tuple[List[str], List[List[Any]]]:
        headers = list(select_result[0].keys())
        items = [[item for item in list(dict_.values())] for dict_ in select_result]
        return headers, items

    # def view_items(self, result):
    #     for x in res:
    #         print(x)
    #     if (flag == "offer" and self.user.role == 2) or (flag == "request" and self.user.role == 1):
    #         ans = input("Do you want to accept any item?(y - yes, n - no)")
    #         if ans == "y":
    #             self.accept_item()
    #         elif ans == "n":
    #             self.user_menu()
    #         else:
    #             print("Incorrect input")

    def accept_item(self):
        # item_id = self.db.accept_item(ans, self.user.id)
        while True:
            ans = self.ans_int("Enter number of the item you want to accept: ")
            user_id, err = self.db.del_item(ans)
            if not user_id:
                print("Incorrect input(probably wrong number) ")
                continue
            else:
                break
        # self.print_item(self.db.select_items("offer"))
        # self.print_item(self.db.select_items("request"))
        self.db.plus_rate(self.user.id, 5)
        print("Thank you for using our market, you've just gained 5 points to your rating.\n"
              "You may give or take 10 rating points to the user, you've just made a deal with. (y - yes, n - no) ")
        ans = input()
        if ans == "y":
            while True:
                pt = self.ans_int("Enter number of points you want to give(from - 10 to 10) ")
                if -10 <= pt <= 10:
                    self.db.plus_rate(user_id['user_id'], pt)
                    break
                else:
                    print("Incorrect input ")

    def print_item(self, result):
        if result is None:
            print("There are no items ")
            return 1
        headers, items = self.separate_headers_and_items(result)
        print(tabulate(items, headers, tablefmt="pretty"))

    def guest_menu(self):
        print("You've entered as a guest\nPlease, choose your option: ")
        while True:
            print("1) Look at the offers\n2) Look at the requests\n3) Back to the previous menu ")
            ans = self.ans_int()
            match ans:
                case 1:
                    self.print_item(self.db.select_items('offer'))
                    # print("Now let's come back to the start menu")
                case 2:
                    self.print_item(self.db.select_items('request'))
                    # print("Now let's come back to the start menu")
                case 3:
                    self.start(True)
                case _:
                    print("Incorrect input ")

    def view_par(self):
        album = Album()
        edition = Edition()
        while True:
            ans = input("Enter the item's type(1 - offer, 2 - request) ")
            if ans in ('1', '2'):
                break
        type_it: str
        order: int
        if ans == "1":
            type_it = "offer"
        elif ans == "2":
            type_it = "request"
        ans = input("Enter the album's title(if you dont want to filter by the parameter - enter 1) : ").title()
        if ans != "1": album.title = ans
        ans = input("Enter the album's artist(if you dont want to filter by the parameter - enter 1) : ").title()
        if ans != "1": album.artist = ans
        ans = self.ans_int("Enter the album's release year(if you dont want to filter by the parameter - enter 1) : ")
        if ans != 1: album.release_year = ans
        ans = input("Enter the album's genre(if you dont want to filter by the parameter - enter 1) : ").title()
        if ans != "1": album.genre = ans
        print("Then, let's specify the exact edition you want to sell or buy ")
        ans = input("Enter the edition's label(if you dont want to filter by the parameter - enter 1) : ").title()
        if ans != "1": edition.label = ans
        ans = self.ans_int("Enter the edition's year(if you dont want to filter by the parameter - enter 1) : ")
        if ans != 1: edition.year = ans

        bounds = None
        while True:
            ans = input("Want to make bounds of price?(y - yes, n- no) ")
            if ans in ('y', 'Y'):
                while True:
                    try:
                        bounds = tuple(
                            map(int, list(input("Enter lower and upper bounds of price(100 200 for example)").split())))
                        break
                    except TypeError and ValueError:
                        continue
                break
            elif ans in ("n", "N"):
                break
            else:
                print("Incorrect input")
                continue
        while True:
            ans = input(
                "Do you want editions to be remastered? (y - yes, n - no, 1 -if you dont want to filter by this) ")
            match ans:
                case "y":
                    edition.is_remastered = True
                    break
                case "n":
                    edition.is_remastered = False
                    break
                case "1":
                    break
                case _:
                    print("Your input is incorrect")
        ans = input("Do you want to order by price instead of default order?(y - yes, n - no)")

        match ans:
            case "y" | "Y":
                while True:
                    ans = self.ans_int("1) Ascending order, 2) Descending order")
                    if ans == 1:
                        order = 1
                        break
                    elif ans == 2:
                        order = 2
                        break
                    else:
                        print("Incorrect input")
                        continue
            case "n" | "N":
                order = 0
        result, err = self.db.select_param(edition, album, order, type_it, bounds)
        print(err)
        self.print_item(result)
        if self.user.role == 1 and type_it == "request" or self.user.role == 2 and type_it == "offer":
            print("Do you want to accept any item? (y - yes, n - no) ")
            while True:
                ans = input()
                match ans:
                    case 'y' | 'Y':
                        self.accept_item()
                        break
                    case 'n' | 'N':
                        break
                    case _:
                        print("Incorrect input ")

    def my_items(self):
        result, err = self.db.select_all_items(self.user.id)
        if result is None:
            print("You dont have items yet ")
        self.print_item(result)
        ans = self.ans_int("Want to delete any of your items? Enter the id, otherwise - enter 0 ")
        res, err = self.db.del_item(ans, self.user.id)
        if res is not None:
            print("Deletion completed")
        else:
            print("Something went wrong(you probably entered wrong number) ")

    def user_menu(self):
        print("You've entered as a ", "seller\n" if self.user.role == 1 else "buyer\n",
              "Please, choose your option: ")
        while True:
            print("1) Look at the offers\n2) Look at the requests\n3) Create a", end='')
            print("n offer" if self.user.role == 1 else " request ")
            print("4) Update an item\n5) Look at your items\n6)Look at the items by parameters\n"
                  "7) Log out\n8) Back to the start menu ")
            ans = self.ans_int()
            match ans:
                case 1:
                    result = self.db.select_items('offer')
                    if not result:
                        print("Offer list is empty ")
                        continue
                    self.print_item(result)
                    if self.user.role != 2:
                        continue
                    print("Do you want to accept any offer? (y - yes, n - no) ")
                    while True:
                        ans = input()
                        match ans:
                            case 'y' | 'Y':
                                self.accept_item()
                                break
                            case 'n' | 'N':
                                break
                            case _:
                                print("Incorrect input ")

                case 2:
                    result = self.db.select_items('request')
                    if not result:
                        print("Request list is empty ")
                        continue
                    self.print_item(result)
                    if self.user.role != 1:
                        continue
                    print("Do you want to accept any request? (y - yes, n - no) ")
                    while True:
                        ans = input()
                        match ans:
                            case 'y' | 'Y':
                                self.accept_item()
                                break
                            case 'n' | 'N':
                                break
                            case _:
                                print("Incorrect input ")
                case 3:
                    self.create_item()
                case 4:
                    self.update_item()
                case 5:
                    self.my_items()
                    continue
                case 6:
                    self.view_par()
                case 7:
                    self.user.role = None
                    if self.user.id:
                        self.db.log_out(self.user.id)
                    break
                case 8:
                    self.start(True)
                case _:
                    print("Incorrect input ")

    def admin_menu(self):
        print("You've entered as an admin. Please, choose your option: ")
        while True:
            ans = self.ans_int("1) View all users\n2) Come back to the starting menu  ")
            match ans:
                case 1:
                    result = self.db.select_all_users()
                    if not result:
                        return
                    self.print_item(result)
                    while True:
                        ans = self.ans_int(
                            "If you want to see all items by a specific user, enter his/her id, enter 0 otherwise ")
                        if ans != 0:
                            user_id = ans
                            res, err = self.db.select_all_items(ans)
                            if err is not None:
                                print(err)
                                continue
                            if res is None:
                                print("No items by this user ")
                                continue
                            self.print_item(res)
                            ans = self.ans_int(
                                "1)If you want to ban specific item and take 30 rating points from user\n2) If you want to "
                                "ban a user\n3) Come back to the main admin menu ")
                            match ans:
                                case 1:
                                    self.db.plus_rate(user_id, -30)
                                    while True:
                                        item_id = self.ans_int("Enter the id of the item ")
                                        res, err = self.db.del_item(item_id)
                                        if res is None:
                                            print("Wrong item id ")
                                            continue
                                        break
                                case 2:
                                    ans = input("Is this final decision? (y - yes, n - no) ")
                                    if ans == "y":
                                        err_us = self.db.del_user(user_id)
                                        err_it = self.db.del_item(user_id)
                                        if err_us is not None and err_it is not None:
                                            print(err_us)
                                            print(err_it)
                                        else:
                                            break
                        else:
                            break
                    break
                case _:
                    return


    def sign_up(self):
        while True:
            login = input("Enter login ")
            self.user.login = login
            self.user.password = input("Enter password ")
            # self.user.password = password
            while True:
                ans = self.ans_int("Enter your role(1 - seller, 2 - buyer) ")
                match ans:
                    case 1:
                        self.user.role = 1  # seller

                    case 2:
                        self.user.role = 2  # buyer

                    case _:
                        print("Incorrect input ")
                        continue
                err = self.db.insert_user(self.user)
                if err is not None:
                    print(err)
                    print("Incorrect input data, try again(try another login ) ")
                    continue
                return

    def sign_in(self):
        while True:
            login = input("Enter login ")
            password: str = input("Enter password ")
            self.user, error = self.db.select_user(login, password)
            if error is not None or self.user is None:
                ans = self.ans_int("Incorrect login or password, want to try again?(1 - yes, 2 - no) ")
                match ans:
                    case 1:
                        continue
                    case 2:
                        return
            # print(self.user.role)
            match self.user.role:
                case 1 | 2:
                    self.user_menu()
                    # self.user.is_online = True
                    return
                case 3:
                    self.admin_menu()
                    # self.user.is_online = True
                    return
                case _:
                    print("User type undefined error ")
                    return

    def start(self, flag=False):
        if not flag:
            print("Welcome to the shop of physical music editions ")
        while True:
            print("Chose an option:\n1) Sign in\n2) Sign up\n3) Stay a guest\n4) Exit ")
            ans = self.ans_int()
            match ans:
                case 1:
                    self.sign_in()
                case 2:
                    self.sign_up()
                case 3:
                    self.guest_menu()
                case 4:
                    try:
                        if self.user.id is not None: self.db.log_out(self.user.id)
                    except AttributeError:
                        pass
                    exit()


    def test(self, t_id):
        self.db.select_one_item(t_id)


if __name__ == '__main__':
    interface = Interface()
    # print(interface.user.is_online)
    # interface.test(2)
    interface.start()
