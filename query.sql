SELECT host, user, authentication_string FROM mysql.user;

CREATE USER 'guest'@'%';
GRANT select,delete,update,insert ON imdb.* TO guest@'%';

DROP USER guest@'localhost';

FLUSH PRIVILEGES;