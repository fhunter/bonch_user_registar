PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (id auto primary key, username text unique, fio text,studnum text, photo blob);
COMMIT;
