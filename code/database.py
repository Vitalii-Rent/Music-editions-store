from model import *
import mysql.connector
import hashlib
from typing import List, Tuple, Any


class DataBase:
    # item = model.Item()
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="200327vital",
            database="music_shop"
        )
        self.mycursor = self.db.cursor(dictionary=True)

    @staticmethod
    def hash(password: str):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


    def log_out(self, user_id):
        query = "update music_shop.user_list SET is_online = 0 WHERE id = %s"
        try:
            self.mycursor.execute(query, (user_id, ))
            self.db.commit()
        except mysql.connector.Error as err:
            print("err")
            print(err)
            return err


    def select_user(self, login, password: str):
        query = "select * from music_shop.user_list where login = %s and password_hash = %s"
        val = (login, self.hash(password))
        try:
            self.mycursor.execute(query, val)
            result = self.mycursor.fetchall()
            if not result: return None, None
            online = "update music_shop.user_list SET is_online = 1 WHERE id = %s"
            user_id = (result[0]['id'],)
            self.mycursor.execute(online, user_id)
            self.db.commit()

        except mysql.connector.Error as err:
            print("error ")
            return None, err
        return self.__fetch_user_result(result)

    @staticmethod
    def __fetch_item(res):
        item = (Album(), Edition())
        print(res)
        item[0].title = res['album_title']
        item[0].artist = res['title']
        item[0].release_year = res['release_year']
        item[0].genre = res['genre']
        item[1].label = res['Label']
        item[1].year = res['edition_year']
        item[1].price = res['price']
        item[1].is_remastered = res['is_remastered']
        print("done ")
        return res, item, None

    @staticmethod
    def __fetch_user_result(result):
        user = User()
        user.id = result[0]['id']
        user.login = result[0]['login']
        user.password = result[0]['password_hash']
        user.is_online = True
        user.rating = result[0]['user_rating']
        user.role = result[0]['role']
        return user, None

    def select_items(self, item_type):
        # query = "select * from music_shop.items_list where type = %s"
        query = "select items_list.id, items_list.type, artist_list.title,album_list.album_title, album_list.release_year, " \
                "album_list.genre, label_list.title as 'Label', edition_list.edition_year, items_list.price, is_remastered," \
                "user_list.login, user_list.user_rating" \
                " from music_shop.items_list " \
                "Inner JOIN music_shop.edition_list ON items_list.edition_id = edition_list.id " \
                "Inner JOIN music_shop.album_list ON edition_list.album_id = album_list.id " \
                "INNER JOIN music_shop.artist_list ON album_list.artist_id = artist_list.id " \
                "INNER JOIN music_shop.label_list ON edition_list.label_id = label_list.id " \
                "INNER JOIN music_shop.user_list ON items_list.user_id = user_list.id " \
                "WHERE items_list.type = %s;"
        try:
            val = (item_type,)
            self.mycursor.execute(query, val)
            result = self.mycursor.fetchall()
            if not result: return result
            return result
        except mysql.connector.Error as err:
            print("err ")
            return err

    def select_all_items(self, user_id):
        # query = "select * from music_shop.items_list where user_id = %s"
        query = "select items_list.id, artist_list.title,album_list.album_title, album_list.release_year, " \
                "album_list.genre, label_list.title as 'Label', edition_list.edition_year, items_list.price, is_remastered, " \
                "user_list.login, user_list.user_rating" \
                " from music_shop.items_list " \
                "Inner JOIN music_shop.edition_list ON items_list.edition_id = edition_list.id " \
                "Inner JOIN music_shop.album_list ON edition_list.album_id = album_list.id " \
                "INNER JOIN music_shop.artist_list ON album_list.artist_id = artist_list.id " \
                "INNER JOIN music_shop.label_list ON edition_list.label_id = label_list.id " \
                "INNER JOIN music_shop.user_list ON items_list.user_id = user_list.id " \
                "WHERE items_list.user_id = %s;"
        try:
            val = (user_id,)
            self.mycursor.execute(query, val)
            result = self.mycursor.fetchall()
            # headers, items = self.separate_headers_and_items(result)
            # print(tabulate(items, headers, tablefmt="pretty"))
            if not result: return None, None
            return result, None
        except mysql.connector.Error as err:
            return None, err

    def update_item(self, item, item_id, it_type, user_id):
        try:
            self.del_item(item_id)
            result, err = self.insert_item(it_type, user_id, item[0], item[1])
        except mysql.connector.Error as err:
            return None, err
        return result, None

    def select_one_item(self, item_id, flag=None):
        query = "select artist_list.title, album_list.album_title, album_list.release_year, " \
                "album_list.genre, label_list.title as 'Label', edition_list.edition_year, items_list.price, is_remastered, " \
                "user_list.login, user_list.user_rating" \
                " from music_shop.items_list " \
                "Inner JOIN music_shop.edition_list ON items_list.edition_id = edition_list.id " \
                "Inner JOIN music_shop.album_list ON edition_list.album_id = album_list.id " \
                "INNER JOIN music_shop.artist_list ON album_list.artist_id = artist_list.id " \
                "INNER JOIN music_shop.label_list ON edition_list.label_id = label_list.id " \
                "INNER JOIN music_shop.user_list ON items_list.user_id = user_list.id " \
                "WHERE items_list.id = %s;"
        try:
            val = (item_id,)
            self.mycursor.execute(query, val)
            result = self.mycursor.fetchone()
            if not result: return None, None, None
            if not flag: return self.__fetch_item(result)
        except mysql.connector.Error as err:
            print(err)
            return None, None, err
        return result, None
        # return self.__fetch_item(result)

    def order_by(self, val):
        pass

    def select_param(self, edition: Edition, album: Album, order: int, type: str, bounds):

        query = "select items_list.id, artist_list.title, album_list.album_title, album_list.release_year, " \
                "album_list.genre, label_list.title as 'Label', edition_list.edition_year, items_list.price, is_remastered, " \
                "user_list.login, user_list.user_rating " \
                "from music_shop.items_list " \
                "Inner JOIN music_shop.edition_list ON items_list.edition_id = edition_list.id " \
                "Inner JOIN music_shop.album_list ON edition_list.album_id = album_list.id " \
                "INNER JOIN music_shop.artist_list ON album_list.artist_id = artist_list.id " \
                "INNER JOIN music_shop.label_list ON edition_list.label_id = label_list.id " \
                "INNER JOIN music_shop.user_list ON items_list.user_id = user_list.id "
        query += " WHERE "
        values = []
        query_where = ""
        query_where += f" items_list.type = %s "
        values.append(type)
        if album.artist:
            query_where += f"and artist_list.title = %s "
            values.append(album.artist)
        if album.title:
            query_where += f"and album_list.album_title = %s "
            values.append(album.title)
        if album.genre:
            query_where += f"and album_list.genre = %s "
            values.append(album.genre)
        if album.release_year:
            query_where += f"and album_list.release_year = %s "
            values.append(album.release_year)
        if edition.label:
            query_where += f"and label_list.title = %s "
            values.append(edition.label)
        if edition.year:
            query_where += f"and edition_list.edition_year = %s "
            values.append(edition.year)
        if edition.is_remastered is not None:
            query_where += f"and edition_list.is_remastered = %s "
            values.append(edition.is_remastered)
        if bounds:
            query_where += f"and items_list.price >= %s and items_list.price <= %s "
            values.append(bounds[0])
            values.append(bounds[1])
        query += query_where
        if order:
            query += f" ORDER BY music_shop.items_list.price "
            if order == 2: query += "DESC;"
        try:
            self.mycursor.execute(query, tuple(values))
            result = self.mycursor.fetchall()
            return result, None
        except mysql.connector.Error as err:
            print(err)
            return None, err

    def is_artist(self, val):
        query = "SELECT id FROM music_shop.artist_list WHERE title=%s"
        self.mycursor.execute(query, (val,))
        result = self.mycursor.fetchone()
        if result:
            return result['id']
        else:
            return None

    def is_label(self, val):
        query = "SELECT id FROM music_shop.label_list WHERE title=%s"
        self.mycursor.execute(query, (val,))
        result = self.mycursor.fetchone()
        if result:
            return result['id']
        else:
            return None

    def is_album(self, album: Album, artist_id):
        query = "SELECT album_list.id FROM music_shop.album_list " \
                "WHERE album_title = %s and  album_list.artist_id = %s and release_year = %s and genre = %s"
        val = (album.title, artist_id, album.release_year, album.genre)
        self.mycursor.execute(query, val)
        result = self.mycursor.fetchone()
        if result is None:
            return None
        else:
            return result['id']

    def is_edition(self, edition: Edition, album_id, label_id):
        query = "SELECT edition_list.id FROM music_shop.edition_list  " \
                "WHERE music_shop.edition_list.album_id = %s and edition_year = %s" \
                " and label_id = %s and is_remastered = %s"
        val = (album_id, edition.year, label_id, edition.is_remastered)
        self.mycursor.execute(query, val)
        result = self.mycursor.fetchone()
        if result is None:
            return None
        else:
            return result['id']

    def insert_item(self, it_type, user_id, album: Album, edition: Edition):
        artist_id = self.is_artist(album.artist)
        # print(artist_id)
        if artist_id is None:
            query = "INSERT INTO music_shop.artist_list (title) VALUES (%s)"
            self.mycursor.execute(query, (album.artist,))
            self.db.commit()
            artist_id = self.mycursor.lastrowid
        album_id = self.is_album(album, artist_id)
        # print(album_id)
        if album_id is None:
            query_album = "INSERT INTO music_shop.album_list (album_title, artist_id, release_year, genre) " \
                          "VALUES (%s, %s, %s, %s)"
            val = (album.title, artist_id, album.release_year, album.genre)
            self.mycursor.execute(query_album, val)
            self.db.commit()
            album_id = self.mycursor.lastrowid
            # print(album_id)
        label_id = self.is_label(edition.label)
        # print(label_id)
        if label_id is None:
            query = "INSERT INTO music_shop.label_list(title) VALUES (%s)"
            self.mycursor.execute(query, (edition.label,))
            self.db.commit()
            label_id = self.mycursor.lastrowid

        edition_id = self.is_edition(edition, album_id, label_id)
        # print(edition_id)
        if edition_id is None:
            query_edition = "INSERT INTO music_shop.edition_list (album_id, edition_year, label_id, is_remastered)" \
                            "VALUES (%s, %s, %s, %s)"
            val = (album_id, edition.year, label_id, edition.is_remastered)
            self.mycursor.execute(query_edition, val)
            self.db.commit()
            edition_id = self.mycursor.lastrowid
            # print(edition_id)
        query_item = "INSERT INTO music_shop.items_list ( type, price, user_id, edition_id)" \
                     "VALUES (%s, %s, %s, %s)"
        val = (it_type, edition.price, user_id, edition_id)
        # print(val)
        self.mycursor.execute(query_item, val)
        self.db.commit()
        item_id = self.mycursor.lastrowid
        return self.select_one_item(item_id, flag=True)

    def insert_user(self, user: User):
        query = "INSERT INTO music_shop.user_list (login, password_hash, is_online, user_rating, role)" \
                " VALUES (%s, %s, %s, %s, %s)"
        val = (user.login, self.hash(user.password), 1, user.rating, user.role)
        try:
            self.mycursor.execute(query, val)
            self.db.commit()
            # result = self.mycursor.fetchall()
        except mysql.connector.Error as err:
            return err
        return None

    def accept_item(self, num, user_id: int):
        pass

    def del_item(self, item_id=None, user_id=None):
        if item_id is None and user_id is not None:
            query = "DELETE FROM music_shop.items_list WHERE user_id=%s"
            try:
                self.mycursor.execute(query, (user_id,))
                self.db.commit()
                return None
                # result = self.mycursor.fetchone()
            except mysql.connector.Error as err:
                return err
        if user_id:
            query_del = "DELETE FROM music_shop.items_list WHERE id=%s and items_list.user_id = %s"
            query_sel = "SELECT user_id FROM music_shop.items_list WHERE id = %s and items_list.user_id = %s"
        else:
            query_del = "DELETE FROM music_shop.items_list WHERE id=%s"
            query_sel = "SELECT user_id FROM music_shop.items_list WHERE id = %s"

        try:
            if user_id:
                val = (item_id, user_id)
            else:
                val = (item_id,)
            self.mycursor.execute(query_sel, val)
            result = self.mycursor.fetchone()
            self.mycursor.execute(query_del, val)
            self.db.commit()
            return result, None
        except mysql.connector.Error as err:
            return None, err

    def del_user(self, user_id):
        query = "DELETE FROM music_shop.user_list WHERE id=%s"
        try:
            self.mycursor.execute(query, (user_id,))
            self.db.commit()
            # result = self.mycursor.fetchone()
        except mysql.connector.Error as err:
            return err
        return None

    def plus_rate(self, user_id, pt):
        query_rate = "SELECT user_rating FROM music_shop.user_list WHERE id = %s"
        query_upd = "UPDATE music_shop.user_list SET user_rating=%s WHERE id=%s"
        try:
            self.mycursor.execute(query_rate, (user_id,))
            old_rate = self.mycursor.fetchone()
            rate = old_rate['user_rating'] + pt
            self.mycursor.execute(query_upd, (rate, user_id))
            self.db.commit()
            return None
        except mysql.connector.Error as err:
            return err

    def select_all_users(self):
        query = "SELECT * FROM music_shop.user_list"
        self.mycursor.execute(query)
        res = self.mycursor.fetchall()
        return res
