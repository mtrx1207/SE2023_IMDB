# [SE17] IMDB - 2023
There are 2 main folders and a database file:
- **data.sql**: our all databases. Attention! You **MUST** do the following things before running the program: 
  1. Make sure to IMPORT this file to your MySQL local database. Steps:
    - Open MySQL, login to your database.
    - Create a database schema called 'imdb'
    - Click 'Server' on the menubar, then 'Data Import'
    - Choose 'Import from Self-Contained File' and look for 'data.sql' 
    - At 'Default Target Schema', choose 'imdb'
    - Click 'Start Import' button.
  2. Change *local_database* variable in __init__.py to be your local database path.
  3. Install all necessary Python modules by typing "pip install [modulename]" in your terminal. The warning will guide you what to do.
  
- **Backend**
  - main.py: our Python Flask file. Run the entire program from here.
  - website folder: other python files, connect flask to database, and render html
    - __init__.py: database setup and initialization (to run the porject, connect to your mysql local database by changing local_database path
    - models.py: create database table and its entities
    - auth.py: accept request from HTML and do backend task (for example: SQL command)
- **Frontend**
  - static folder: include images, CSS, and Javascript file
    - image folder: 
      - home folder: contains movie posters with aspect 2:1
      - poster folder: contains movie posters with aspect 3:4
      - icons folder: contains icons
      - website logo
    - login.css: styling for login page
    - signup.css: styling for signup page
    - header.css: styling for header
    - home.css: styling for home page
    - search.css: styling for search result page
    - movie.css: styling for movie info, statistics, and comments page
    - watched.css: styling for watched page
    - watchlist.css; styling for watchlist page
    - database.css: styling for database admin page
    - database.js: javascript for database admin page
    - header.js: javascript for header
    - home.js: javascript for home page
    - movie.js: javascript for movie page
   
  - templates folder: include HTML files
    - login.html: login page
    - signup.html: signup page
    - header.html: header for each page, contains menu bar, search bar, and login/logout button
    - home.html: home page
    - search.html: search result page
    - movie.html: contains all informations of a movie and user reviews
    - watched.html: watched page
    - watchlist.html: watchlist page
    - database.html: *only admins can access this page to edit database

  *do not change static and templates folder name, otherwise our Flask can't find our HTML file.*
  
  Author: 公泽尘，徐祥龙，黄程骏，董云帆，吕汪洋
