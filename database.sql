PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (id auto primary key, username text unique, fio text,studnum text, photo blob);
CREATE TABLE queue (id auto primary key, username text not null, password text not null, date datetime not null default current_timestamp, done boolean not null default 'false');
COMMIT;
