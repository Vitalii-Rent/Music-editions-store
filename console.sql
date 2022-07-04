/*CREATE table music_shop.user
(
    ID        INT PRIMARY KEY AUTO_INCREMENT,
    FirstName nvarchar(50) not null,
    LastName  nvarchar(50)
);*/
/*CREATE table music_shop.role
(
    role_id   INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL,
    FOREIGN KEY (role_id) REFERENCES music_shop.user_role (role_id)
);*/
CREATE DATABASE music_shop;
CREATE TABLE music_shop.user_list
(
    id            INT PRIMARY KEY AUTO_INCREMENT,
    login         VARCHAR(64) UNIQUE,
    password_hash CHAR(64),
    is_online     BIT DEFAULT 0,
    user_rating   INT DEFAULT 0,
    role          INT NOT NULL,
    FOREIGN KEY (role) REFERENCES music_shop.roles (id) ON DELETE CASCADE
);





CREATE TABLE music_shop.roles
(
    id        INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(20)
);


/*CREATE TABLE music_shop.users_roles
(
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES music_shop.user_list (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES music_shop.user_role (id) ON DELETE CASCADE
);*/
CREATE TABLE music_shop.artist_list
(
    id    INT PRIMARY KEY AUTO_INCREMENT,
    title NVARCHAR(30)
);

CREATE TABLE music_shop.album_list
(
    id           INT PRIMARY KEY AUTO_INCREMENT,
    album_title  NVARCHAR(100),
    artist_id    INT,
    #genre_title NVARCHAR(30),
    release_year INT,
    genre        NVARCHAR(100),
    FOREIGN KEY (artist_id) REFERENCES music_shop.artist_list (id) ON DELETE CASCADE
);



CREATE TABLE music_shop.label_list
(
    id    INT PRIMARY KEY AUTO_INCREMENT,
    title NVARCHAR(30)
);
CREATE TABLE music_shop.edition_list
(
    id             INT PRIMARY KEY AUTO_INCREMENT,
    album_id       INT NOT NULL,
    edition_year   INT,
    label_id       INT,
    is_remastered  BIT,
    FOREIGN KEY (album_id) REFERENCES music_shop.album_list (id) ON DELETE CASCADE,
    FOREIGN KEY (label_id) REFERENCES music_shop.label_list (id) ON DELETE CASCADE
);




CREATE TABLE music_shop.items_list
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    type        ENUM ('request', 'offer') NOT NULL,
    user_id     INT                       NOT NULL,
    #user_rating int                       NOT NULL,
    edition_id  INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price       INT,
    FOREIGN KEY (user_id) REFERENCES music_shop.user_list (id) ON DELETE CASCADE,
    #FOREIGN KEY (user_rating) REFERENCES music_shop.user_list (user_rating) ON DELETE CASCADE,
    FOREIGN KEY (edition_id) REFERENCES music_shop.edition_list (id) ON DELETE CASCADE
);


CREATE TABLE music_shop.items_archive
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    type        ENUM ('request', 'offer') NOT NULL,
    user_id     INT                       NOT NULL,
    #user_rating int                       NOT NULL,
    edition_id  INT                       NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price       INT,
    FOREIGN KEY (user_id) REFERENCES music_shop.user_list (id) ON DELETE CASCADE,
    #FOREIGN KEY (user_rating) REFERENCES music_shop.user_list (user_rating) ON DELETE CASCADE,
    FOREIGN KEY (edition_id) REFERENCES music_shop.edition_list (id) ON DELETE CASCADE
);


/*CREATE TABLE music_shop.genre_list
(
    id    INT PRIMARY KEY AUTO_INCREMENT,
    title NVARCHAR(30)
    #FOREIGN KEY (title) REFERENCES music_shop.albums_genres(genre) ON DELETE CASCADE
);*/


/*CREATE TABLE music_shop.albums_genres
(
    album_id INT,
    genre_id INT,
    FOREIGN KEY (album_id) REFERENCES music_shop.album_list (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES music_shop.genre_list (id) ON DELETE CASCADE
);*/
#USE music_shop;
#

CREATE TRIGGER trg_items_archive
    AFTER DELETE
    ON music_shop.items_list
    FOR EACH ROW
BEGIN
    INSERT music_shop.items_archive(id,
                                    type,
                                    user_id,
                                    edition_id,
                                    create_date,
                                    price)
    VALUES (OLD.id,
            OLD.type,
            OLD.user_id,
            OLD.edition_id,
            OLD.create_date,
            OLD.price);
    #FROM music_shop.items_list old
    #WHERE music_shop.items_list.id=id;
END;

CREATE PROCEDURE music_shop.insert_proc(new_type ENUM ('request', 'offer'), new_user_id INT, new_edition_id INT,
                                        new_price INT)
BEGIN
    INSERT INTO music_shop.items_list(type, user_id, edition_id, price)
    VALUES (new_type, new_user_id, new_edition_id, new_price);
end;

INSERT INTO music_shop.user_list(login, password_hash)
VALUES ('user', '1234');

INSERT INTO music_shop.album_list(album_title)
VALUES ('Get Back');

INSERT INTO music_shop.edition_list(album_id)
VALUES ('1');

CALL music_shop.insert_proc('request', '1', '1', '400');



CREATE PROCEDURE music_shop.update_proc(upd_id INT, upd_login NVARCHAR(32), upd_password_hash NVARCHAR(32),
                                        upd_is_online BIT, upd_user_rating INT)
BEGIN
    UPDATE music_shop.user_list
    SET login=upd_login,
        password_hash=upd_password_hash,
        is_online=upd_is_online,
        user_rating=upd_user_rating
    WHERE id = upd_id;
end;

CALL update_proc('1', 'eretr', '1234', 1, '5');

CREATE PROCEDURE music_shop.delete_proc(del_id INT)
BEGIN
    DELETE
    FROM items_list
    WHERE id = del_id;
end;

CALL delete_proc(5);
#SET GLOBAL log_bin_trust_function_creators = 0;
CREATE FUNCTION music_shop.best_rate_rsd()
    RETURNS INT
    READS SQL DATA
BEGIN
    DECLARE MAX INT DEFAULT NULL;
    SELECT MAX(music_shop.user_list.user_rating) FROM user_list INTO MAX;
    RETURN MAX;
end;

SELECT music_shop.best_rate();
#select * from music_shop.user

CREATE VIEW view_1 as
select *
from items_archive;

CREATE VIEW view_2 as
select *
from items_archive
where price > 100;

CREATE VIEW view_3 as
select *
from items_archive
WHERE price > 100
  and type = 'offer';

CREATE VIEW view_4 as
select id, user_id, type, price
from items_archive;

CREATE VIEW view_5 as
select type as 'Type of the item', price as 'Price of the item'
from items_archive;

CREATE VIEW view_6 as
select id, CONCAT('User with ID ', user_id, ' made a/an ', type, ' priced ', price) as info
from items_archive;

CREATE VIEW view_7 as
select SUM(CASE when type = 'offer' then price else 0 end)   as 'Sum of offers',
       SUM(CASE when type = 'request' then price else 0 end) as 'Sum of requests'
from items_archive;

CREATE view view_8 as
select *
from items_archive
limit 5;

CREATE view view_9 as
select *
from items_archive
order by RAND()
limit 5;

CREATE view view_10 as
select *
from items_archive
where price is NULL
   or edition_id is NULL;

CREATE view view_11 as
select *
from user_list
where login like '%ere';

CREATE view view_12 as
select *
from items_archive
ORDER BY price DESC;

CREATE view view_13 as
select *
from items_archive
ORDER BY create_date, price DESC;

CREATE view view_14 as
select *
from user_list
ORDER BY SUBSTRING(login, 2);

CREATE view view_15 as
select *
from items_archive
ORDER BY create_date, price is NULL;

SELECT *
from view_15;


CREATE view view_16 as
select *
from items_archive
ORDER BY CASE WHEN price IS NOT NULL then price ELSE create_date END;

CREATE view view_17 as
select album_title, artist_id
from album_list
union all
select '-------', '--------'
union all
select login, user_rating
from user_list;


CREATE view view_18 as
select album_list.album_title, artist_list.title
from album_list,
     artist_list
where album_list.artist_id = artist_list.id;

CREATE or replace view view_19 as
select items_list.id, items_list.type, items_list.user_id, items_list.price
from items_list
         join items_archive
              ON (items_list.type = items_archive.type and items_list.user_id = items_archive.user_id and
                  items_list.price = items_archive.price);


/*INSERT INTO items_list ( items_list.type, items_list.user_id, items_list.price)
 VALUES ('request', '2', '500');

INSERT INTO user_list ( login, password_hash,user_rating)
 VALUES ('not_so_progressive_rocker', '12345', '9');*/

CREATE OR REPLACE view view_20 as
select user_list.id, user_list.login
from user_list
where NOT Exists(SELECT user_id from items_list WHERE user_list.id = items_list.user_id);

select *
from view_20;

CREATE or replace view view_21 as
select items_list.*
from items_list
         LEFT OUTER JOIN items_archive
                         ON items_list.user_id = items_archive.user_id
where items_archive.user_id IS NULL;



CREATE or replace view view_22 as
select items_list.type, items_archive.price, ul.user_rating
from items_list
         join items_archive
              ON (items_list.user_id = items_archive.user_id and items_list.type = items_archive.type)
         JOIN user_list ul on items_list.user_id = ul.id and ul.user_rating <= 10;

CREATE or replace view view_23 as
select user_list.id,
       user_list.login,
       (select SUM(price) from items_list where items_list.user_id = user_list.id) as Total
from user_list;



CREATE or replace view view_24 as
select login,
       #COUNT(user_id) as 'Number of users'
       SUM(items_list.price) as Total
from user_list
         LEFT OUTER JOIN items_list ON user_list.id = items_list.user_id
GROUP BY login;

CREATE or replace view view_25 as
select items_list.user_id as List, ia.user_id as Archive
from items_list
         LEFT OUTER JOIN items_archive ia on items_list.user_id = ia.user_id
union
select items_list.user_id as List, ia.user_id as Archive
from items_list
         RIGHT OUTER JOIN items_archive ia on items_list.user_id = ia.user_id;


CREATE or replace view view_26 as
select login,
       #COUNT(user_id) as 'Number of users'
       SUM(COALESCE(price, 0) * case when items_list.edition_id IS NULL then 0 ELSE 1 END) as Total
from user_list
         LEFT JOIN items_list ON user_list.id = items_list.user_id
GROUP BY login;

CREATE view view_33 as
select max(price)
from items_list;

CREATE view view_34 as
select count(*)
from artist_list;


CREATE or replace view view_35 as
select count(items_list.edition_id)
from items_list;

CREATE or replace view view_36 as
select il.user_id, il.price, SUM(price) over (ORDER BY price) as Sum
from items_list il;

CREATE or replace view view_37 as
select datediff(create_date_2, create_date_1) as 'Date difference'
from (
         select create_date as create_date_1
         from items_list
         where id = 1) a,
     (
         select create_date as create_date_2
         from items_list
         where id = 3
     ) b;

select *
from view_7;

SHOW GRANTS;

CREATE user 'someuser'@'localhost' identified by 'p4ssword';
grant all privileges on *.* to 'someuser'@'localhost' with grant option;

REVOKE ALL PRIVILEGES, GRANT OPTION FROM
    'someuser'@'localhost';

show grants for 'someuser'@'localhost';

grant select (login, user_rating) on user_list
    to 'someuser'@'localhost';

grant execute on PROCEDURE insert_proc to 'someuser'@'localhost';

show grants for 'someuser'@'localhost';

grant execute on PROCEDURE insert_proc to 'someuser'@'localhost';

drop user 'someuser'@'localhost';

CREATE PROCEDURE proc_1()
begin
    declare rows_number int;

    start transaction;
    select count(*) from items_list into rows_number;
    update items_list as il set il.price = 400 where il.price > 400;
    if (rows_number % 2 = 0) then
        rollback;
        select id, il.price as 'Rolled back prices' from items_list as il;
    else
        commit;
        select id, il.price as 'Committed prices' from items_list as il;
    end if;
end;

CALL proc_1;

CREATE PROCEDURE proc_2(rating int, number int)
begin
    declare rows_number int; select count(*) from user_list into rows_number;
    start transaction; delete from user_list as ul where ul.user_rating < rating;
    if (number > rows_number) then
        rollback; select id, login, user_rating as 'Rolled back users' from user_list;
    else
        commit; select id, login, user_rating as 'Committed users' from user_list;
    end if;
end;

call proc_2(3, 3);

select album_list.album_title, artist_list.title, album_list.release_year,
                 album_list.genre, label_list.title as Label, edition_list.edition_year, items_list.price, is_remastered
from music_shop.items_list
         Inner JOIN music_shop.edition_list
                    ON items_list.edition_id = edition_list.id
         Inner JOIN music_shop.album_list
                    ON edition_list.album_id = album_list.id
         INNER JOIN music_shop.artist_list
                    ON album_list.artist_id = artist_list.id
         INNER JOIN music_shop.label_list
                    ON edition_list.label_id = label_list.id
WHERE items_list.id = 2;



UPDATE music_shop.items_list, music_shop.edition_list, music_shop.album_list, music_shop.label_list, music_shop.artist_list
SET album_title = 'Abbey Road', artist_list.title = 'The Beatles', release_year=1969,
    genre = 'rock', label_list.title='EMI', edition_year = 1987, items_list.price = 200
WHERE items_list.id =2 and items_list.edition_id = edition_list.id and album_id = album_list.id
and edition_list.label_id = label_list.id and album_list.artist_id = artist_list.id;

select id from album_list where id = 2;

SELECT edition_list.id FROM music_shop.edition_list, music_shop.album_list, music_shop.label_list
WHERE music_shop.album_list.album_title = 'Abbey Road' and edition_year = 1987
and music_shop.label_list.title = 'EMI' and is_remastered = TRUE;


select * from music_shop.user_list where login = 'qwerty' and password_hash = '1149559268791570094';