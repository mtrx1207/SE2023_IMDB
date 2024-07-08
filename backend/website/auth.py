from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import connection, c, app
from flask_login import login_user, login_required, logout_user, current_user
import datetime, threading, random, os
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)

def add_to_list(choice, user, movie_id):
    if user.is_authenticated:
        stmt = f"select * from imdb.{choice} where user_id = {user.id} and movie_id = {movie_id}"
        c.execute(stmt)
        res = c.fetchall()
        if len(res)==0:
            stmt = f"insert into imdb.{choice} values ({user.id},{movie_id})"
            c.execute(stmt)
            modify_preference(user.id, movie_id)
            connection.commit()
            if choice == "watched":
                stmt = f"select * from imdb.watchlist where user_id = {user.id} and movie_id = {movie_id}"
                c.execute(stmt)
                res = c.fetchall()
                if len(res)>0:
                    stmt = f"delete from imdb.watchlist where user_id = {user.id} and movie_id = {movie_id}"
                    c.execute(stmt)
                    connection.commit()
            elif choice == "watchlist":
                stmt = f"select * from imdb.watched where user_id = {user.id} and movie_id = {movie_id}"
                c.execute(stmt)
                res = c.fetchall()
                if len(res)>0:
                    stmt = f"delete from imdb.watched where user_id = {user.id} and movie_id = {movie_id}"
                    c.execute(stmt)
                    connection.commit()
            flash(f'Added to {choice}', category='success')
        else:
            if choice == "watchlist":
                flash('This movie already exists in your watchlist', category='error')
            elif choice == "watched":
                flash('This movie is already in your watched movies', category='error')
    else:
        return redirect(url_for('auth.login'))

def modify_preference(user_id, movie_id):
    # get user_preference and movie_genres
    c.execute(f"select * from imdb.user where id = {user_id}")
    user_preference = c.fetchone()[4]
    c.execute(f"select * from imdb.movie where id = {movie_id}")
    movie_genres = c.fetchone()[2]

    # resolve user_preference
    user_preference_list = []
    if len(user_preference) > 0:
        for user_preference_entry in user_preference.split(","):
            user_preference_list.append(user_preference_entry.split(":"))

    # check movie_genres
    movie_genres_list = movie_genres.split(",")
    for genre in movie_genres_list:
        # check if already in user_preference_list
        flag = False
        for user_preference_entry in user_preference_list:
            # if find, just modify
            if user_preference_entry[0] == genre:
                user_preference_entry[1] = str(int(user_preference_entry[1]) + 1)
                flag = True
                break
        # if not find, add new entry
        if flag == False:
            user_preference_list.append([genre, "1"])

    # synthesis user_preference
    user_preference = ""
    flag = True
    for user_preference_entry in user_preference_list:
        if flag : flag = False
        else : user_preference += ","
        user_preference += user_preference_entry[0] + ":" + user_preference_entry[1]

    # write user_preference back
    c.execute(f"update imdb.user SET preference=\"{user_preference}\" where id = {user_id}")


def display(choice, user_id):
    stmt = f"select movie_id from imdb.{choice} where user_id = {user_id}"
    c.execute(stmt)
    movie_id = c.fetchall()
    list = []
    for movie in movie_id:
        stmt = f"select id, image_path from imdb.movie where id = {movie[0]}"
        c.execute(stmt)
        movie = c.fetchone()
        list.append(movie)
    return list

is_admin = 0

@auth.route('/', methods=['GET', 'POST'])
def home():
    # movie popularity recommend_value
    movie_recommend_stat = []

    # get all movies
    c.execute(f"select * from imdb.movie")
    all_movies = c.fetchall()

    # resolve user_preference
    if current_user.is_authenticated:
        if current_user.email == "admin":
            user_preference = ""
        else:
            user_preference = current_user.preference
    else:
        user_preference = ""
    user_preference_list = []
    if len(user_preference) > 0:
        for user_preference_entry in user_preference.split(","):
            user_preference_list.append(user_preference_entry.split(":"))

    # get ignore_movie_list
    ignore_movie_list = []
    if current_user.is_authenticated:
        c.execute(f"select movie_id from imdb.watched where user_id = {current_user.id}")
        watched_id_list = [temp[0] for temp in c.fetchall()]
        c.execute(f"select movie_id from imdb.watchlist where user_id = {current_user.id}")
        watchlist_id_list = [temp[0] for temp in c.fetchall()]
        ignore_movie_list = watched_id_list + watchlist_id_list

    # go through all the movies
    for movie in all_movies:
        # popularity = rating * votes
        popularity = movie[8] * movie[9]

        # check if it's in watchlist or watched
        if movie[0] in ignore_movie_list:
            recommend_value = -1
        else:
            # calculate recommend_value
            movie_genres = movie[2]
            movie_genres_list = movie_genres.split(",")
            recommend_value = 0
            if len(user_preference) > 0:
                for genre in movie_genres_list:
                    # check if it's in user_preference_list
                    for user_preference_entry in user_preference_list:
                        # if find, add recommend_value
                        if user_preference_entry[0] == genre:
                            recommend_value += int(user_preference_entry[1])
                            break
        
        # append to movie_recommend_stat
        movie_recommend_stat.append([movie, popularity, recommend_value])

    # get most_popular
    movie_recommend_stat.sort(key=takeSecondElement, reverse=True)
    most_popular = movie_recommend_stat[0][0]
    # get recommendation
    movie_recommend_stat.sort(key=takeThirdElement, reverse=True)
    recommendation = [temp[0] for temp in movie_recommend_stat[0:4]]

    #sliding poster (randomized for now)
    s = set()
    sliding=[]
    while len(sliding)<4:
        i = random.randint(1,len(all_movies))
        if i not in s:
            s.add(i)
            c.execute(f"select * from imdb.movie where id={i}")
            sliding.append(c.fetchone())

    top_comment = []
    for movie in sliding:
        c.execute(f"select * from imdb.review where movie_id={movie[0]} and likes=(select max(likes) from imdb.review where movie_id={movie[0]})")
        top_comment.append(c.fetchone())

    if request.method == 'POST':
        if request.form.get('movie_id'):
            if current_user.is_authenticated:
                add_to_list("watchlist", current_user, request.form.get('movie_id'))
            else:
                return redirect(url_for('auth.login'))
        elif request.form.get('more_info'):
            movie_id = int(request.form.get('more_info'))
            return redirect(url_for('auth.movie', movie_id=movie_id))
    return render_template("home.html", user=current_user, result=recommendation, sliding=sliding, popular=most_popular, top_comment=top_comment, is_admin=is_admin, filter=filter)

def takeSecondElement(element):
    return element[1]

def takeThirdElement(element):
    return element[2]

@auth.route('/login', methods=['GET', 'POST'])
def login():
    global is_admin
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        admin = Admin.query.first()
        if email == "admin":
            if check_password_hash(admin.password, password): #admin password: 12345678
                flash('Logged in successfully.', category='success')
                login_user(admin, remember=True)
                is_admin = 1
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('auth.login'))
        elif user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    global is_admin
    logout_user()
    is_admin = 0
    return redirect(url_for('auth.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(username)<2:
            flash('Invalid username. Username must be greater than 1 character.', category='error')
        elif len(email)<4:
            flash('Invalid email. Email must be greater than 3 characters.', category='error')
        elif len(password)<8:
            flash('Invalid password. Password must be greater than 7 characters.', category='error')
        elif password!=confirm:
            flash('Passwords don\'t match.', category='error')
        elif email == "admin":
            flash('Unauthorized email. Reserved only for admins', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'), username=username, preference="")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account created successfully.', category='success')
            return redirect(url_for('auth.home'))
    return render_template("signup.html", user=current_user)

query = ""
query_res = []
filter = "All"

def search_query(sort=None, asc_desc=None, filter_by="All"):
    global query, query_res, filter
    filter = filter_by
    if filter == "All":
        if sort==None:
            stmt = f"select * from imdb.movie where (\
                    title regexp '^{query}[^a-zA-Z]' or title regexp '[ ]{query}[^a-zA-Z]' or title regexp '[^a-zA-Z]{query}$' or title regexp '^{query}$'\
                    or description regexp '^{query}[^a-zA-Z]' or description regexp '[ ]{query}[^a-zA-Z]' or description regexp '[^a-zA-Z]{query}$' or description regexp '^{query}$'\
                    or actors regexp '^{query}[^a-zA-Z]' or actors regexp '[ ]{query}[^a-zA-Z]' or actors regexp '[^a-zA-Z]{query}$' or actors regexp '^{query}$'\
                    )"
        else:
            if asc_desc==None:
                stmt = f"select * from imdb.movie where (\
                    title regexp '^{query}[^a-zA-Z]' or title regexp '[ ]{query}[^a-zA-Z]' or title regexp '[^a-zA-Z]{query}$' or title regexp '^{query}$'\
                    or description regexp '^{query}[^a-zA-Z]' or description regexp '[ ]{query}[^a-zA-Z]' or description regexp '[^a-zA-Z]{query}$' or description regexp '^{query}$'\
                    or actors regexp '^{query}[^a-zA-Z]' or actors regexp '[ ]{query}[^a-zA-Z]' or actors regexp '[^a-zA-Z]{query}$' or actors regexp '^{query}$'\
                    ) order by {sort}"
            else:
                stmt = f"select * from imdb.movie where (\
                    title regexp '^{query}[^a-zA-Z]' or title regexp '[ ]{query}[^a-zA-Z]' or title regexp '[^a-zA-Z]{query}$' or title regexp '^{query}$'\
                    or description regexp '^{query}[^a-zA-Z]' or description regexp '[ ]{query}[^a-zA-Z]' or description regexp '[^a-zA-Z]{query}$' or description regexp '^{query}$'\
                    or actors regexp '^{query}[^a-zA-Z]' or actors regexp '[ ]{query}[^a-zA-Z]' or actors regexp '[^a-zA-Z]{query}$' or actors regexp '^{query}$'\
                    ) order by {sort} {asc_desc}"
    else:
        if sort==None:
            stmt = f"select * from imdb.movie where (\
                    {filter} regexp '^{query}[^a-zA-Z]' or {filter} regexp '[ ]{query}[^a-zA-Z]' or {filter} regexp '[^a-zA-Z]{query}$' or {filter} regexp '^{query}$' or {filter} regexp ',{query},'\
                    )"
        else:
            if asc_desc==None:
                stmt = f"select * from imdb.movie where (\
                    {filter} regexp '^{query}[^a-zA-Z]' or {filter} regexp '[ ]{query}[^a-zA-Z]' or {filter} regexp '[^a-zA-Z]{query}$' or {filter} regexp '^{query}$' or {filter} regexp ',{query},'\
                    ) order by {sort}"
            else:
                stmt = f"select * from imdb.movie where (\
                    {filter} regexp '^{query}[^a-zA-Z]' or {filter} regexp '[ ]{query}[^a-zA-Z]' or {filter} regexp '[^a-zA-Z]{query}$' or {filter} regexp '^{query}$' or {filter} regexp ',{query},'\
                    ) order by {sort} {asc_desc}"
    c.execute(stmt)
    query_res = c.fetchall()

@auth.route('/filter', methods=['GET', 'POST'])
def filtering():
    global filter
    filters = json.loads(request.data)
    filter = filters["filter"]
    return redirect(url_for('auth.search'))

@auth.route('/search', methods=['GET', 'POST'])
def search():
    global query
    if request.method == 'GET':
        query = request.args.get('q')
        search_query(filter_by=filter)
    else:
        if request.form.get('watchlist'):
            add_to_list("watchlist", current_user, request.form.get('watchlist'))
        elif request.form.get('watched'):
            add_to_list("watched", current_user, request.form.get('watched'))
        elif request.form.get('alphabetical'):
            search_query('title',filter_by=filter)
        elif request.form.get('highest_rated'):
            search_query('rating', 'desc', filter)
        elif request.form.get('newly_released'):
            search_query('year', 'desc', filter)
    return render_template("search.html", user=current_user, query=query, result=query_res, is_admin=is_admin, filter=filter)

@auth.route('/watchlist', methods=['GET', 'POST'])
@login_required
def watchlist():
    user_id = current_user.id
    list = display("watchlist", user_id)
    if request.method == 'POST':
        if request.form.get('watched'):
            movie_id = request.form.get('watched')
        else:
            movie_id = request.form.get('remove')
        if request.form.get('watched'):
            add_to_list("watched", current_user, movie_id)
        stmt = f"delete from imdb.watchlist where user_id = {user_id} and movie_id = {movie_id}"
        c.execute(stmt)
        connection.commit()
        for movie in list:
            if movie[0]==movie_id:
                list.pop(movie)
        list = display("watchlist", user_id)
    return render_template("watchlist.html", user=current_user, result=list, filter=filter)

@auth.route('/watched', methods=['GET', 'POST'])
@login_required
def watched():
    user_id = current_user.id
    list = display("watched", user_id)
    if request.method == 'POST':
        stmt = f"delete from imdb.watched where user_id = {user_id} and movie_id = {request.form.get('movie_id')}"
        c.execute(stmt)
        connection.commit()
        for movie in list:
            if movie[0]==request.form.get('movie_id'):
                list.pop(movie)
        list = display("watched", user_id)
    return render_template("watched.html", user=current_user, result=list, filter=filter)

@auth.route('/database', methods=['GET', 'POST'])
def database():
    stmt = f"select * from imdb.movie"
    c.execute(stmt)
    movies = c.fetchall()
    return render_template("database.html", user=current_user, movies=movies)

@auth.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    title="";genre="";description="";director="";actors="";year="";runtime="";image_path="";rating="";votes="";five_stars="";four_stars="";three_stars="";two_stars="";one_star=""
    if request.method == 'POST':
        c.execute("select * from imdb.movie")
        all_movies = c.fetchall()
        id = len(all_movies)+1
        title = request.form.get('title')
        genre = request.form.get('genre')
        description = request.form.get('description')
        director = request.form.get('director')
        actors = request.form.get('actors')
        year = request.form.get('year')
        runtime = request.form.get('duration')
        rating = float(request.form.get('rating'))
        votes = int(request.form.get('votes'))
        five_stars = int(request.form.get('five_stars'))
        four_stars = int(request.form.get('four_stars'))
        three_stars = int(request.form.get('three_stars'))
        two_stars = int(request.form.get('two_stars'))
        one_star = int(request.form.get('one_star'))
        print(request.files)
        if 'poster' not in request.files or 'home' not in request.files:
            flash('No file part', category='error')
            return redirect(url_for('auth.database'))
        poster = request.files['poster']
        home = request.files['home']
        if poster.filename == '' or home.filename == '':
            flash('Incomplete images selected for upload', category='error')
            return redirect(url_for('auth.database'))
        if poster.filename != home.filename:
            flash('Different file name', category="error")
            return redirect(url_for('auth.database'))
        if poster and home:
            filename = secure_filename(poster.filename)
            poster.save(os.path.join(app.config['UPLOAD_FOLDER']+'poster', filename))
            home.save(os.path.join(app.config['UPLOAD_FOLDER']+'home', filename))
            flash('Images successfully uploaded', category='success')

        image_path = poster.filename

        if title=="" or genre=="" or description=="" or director=="" or actors=="" or year=="" or runtime=="" or rating=="" or votes=="" or image_path=="" or five_stars=="" or four_stars=="" or three_stars=="" or two_stars=="" or one_star=="":
            flash('All fields must not be empty', category='error')
        else:
            c.execute("insert into imdb.movie values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[id,title,genre,description,director,actors,year,runtime,rating,votes,image_path,five_stars,four_stars,three_stars,two_stars,one_star])
            connection.commit()
    return redirect(url_for('auth.database'))

@auth.route('/search_db', methods=['GET','POST'])
def search_db():
    global query, query_res
    query = request.args.get('q')
    search_query()
    movies = query_res
    return render_template("database.html", movies=movies)

movie_page_res = []
reviews = []
votes = []
lock = threading.Lock()

@auth.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == "POST":
        if current_user.is_authenticated:
            data_received = json.loads(request.data) 
            movie_id = data_received['movie_id']
            vote = int(data_received['vote'])
            user_id = current_user.id
            review_id = data_received['review_id']
            review = Review.query.filter_by(id=review_id).first()
            
            if review:
                stmt = f"select * from imdb.vote where user_id={user_id} and movie_id={movie_id} and review_id={review_id}"
                lock.acquire()
                c.execute(stmt)
                lock.release()
                res = c.fetchone()
                if res:
                    current_state = int(res[3])
                    if current_state>0 and vote == 0:
                        stmt = f"update imdb.review set likes = likes-1 where id={review_id} and movie_id={movie_id}"
                        lock.acquire()
                        c.execute(stmt)
                        lock.release()
                        connection.commit()
                    elif current_state<0 and vote == 0:
                        stmt = f"update imdb.review set likes = likes+1 where id={review_id} and movie_id={movie_id}"
                        lock.acquire()
                        c.execute(stmt)
                        lock.release()
                        connection.commit()
                    stmt = f"update imdb.vote set vote = {vote} where user_id={user_id} and review_id={review_id} and movie_id={movie_id}"
                    lock.acquire()
                    c.execute(stmt)
                    lock.release()
                    connection.commit()
                else:
                    stmt = f"insert into imdb.vote values ({user_id},{movie_id},{review_id},{vote})"
                    lock.acquire()
                    c.execute(stmt)
                    lock.release()
                    connection.commit()
                stmt = f"update imdb.review set likes = likes+{vote} where id={review_id} and movie_id={movie_id}"
                lock.acquire()
                c.execute(stmt)
                lock.release()
                connection.commit()
                return json.dumps({'status' : 'success'})
            return json.dumps({'status' : 'no post found'})
        else:
            return json.dumps({'status' : 'user not logged in'})
    return redirect(url_for(f'/movie/{movie_id}'))

def update_rating(choice, rating, movie_id):
    if rating == 5.0:
        stars = "five_stars"
    elif rating == 4.0:
        stars = "four_stars"
    elif rating == 3.0:
        stars = "three_stars"
    elif rating == 2.0:
        stars = "two_stars"
    else:
        stars = "one_star"
    if choice == "add":
        stmt = f"update imdb.movie set {stars}={stars}+1, votes=votes+1 where id={movie_id}"
    elif choice == "delete":
        stmt = f"update imdb.movie set {stars}={stars}-1, votes=votes-1 where id={movie_id}"
    lock.acquire()
    c.execute(stmt)
    lock.release()
    connection.commit()
    stmt = f"select five_stars, four_stars, three_stars, two_stars, one_star, votes from imdb.movie where id={movie_id}"
    lock.acquire()
    c.execute(stmt)
    lock.release()
    star = c.fetchone()
    new_rating = round((star[0]*5+star[1]*4+star[2]*3+star[3]*2+star[4]*1)/star[5], 1)
    stmt = f"update imdb.movie set rating = {new_rating} where id={movie_id}"
    lock.acquire()
    c.execute(stmt)
    lock.release()
    connection.commit()

@auth.route('/comment/<int:movie_id>', methods=['POST'])
def comment(movie_id):
    if current_user.is_authenticated:
        jsonData = json.loads(request.data)
        rating = float(jsonData['rating'])
        comment = jsonData['comment']
        id = len(reviews)+1
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stmt = f"select * from imdb.review where user_id = {current_user.id} and movie_id = {movie_id}"
        lock.acquire()
        c.execute(stmt)
        lock.release()
        once = c.fetchall()
        if len(once)==0:
            lock.acquire()
            c.execute("insert into imdb.review values (%s,%s,%s,%s,%s,%s,0,%s)",[id,current_user.id,movie_id,current_user.username,rating,comment,date])
            lock.release()
            connection.commit()
            update_rating("add", rating, movie_id)
        else:
            flash('You can only submit 1 review per movie',category='error')
    else:
        return redirect(url_for('auth.login'))
    return redirect(url_for(f'/movie/{movie_id}'))

@auth.route('/delete_comment/<int:movie_id>', methods=['GET', 'POST'])
def delete_comment(movie_id):
    global reviews
    if request.method == "POST":
        review = eval(request.form.get('review_id'))
        stmt = f"delete from imdb.review where id={int(review[0])} and movie_id={movie_id}"
        c.execute(stmt)
        connection.commit()
        update_rating("delete", float(review[4]), movie_id)
    return redirect(url_for('auth.movie', movie_id=movie_id))

@auth.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie(movie_id):
    global movie_page_res, reviews, votes
    if request.method == 'GET':
        stmt = f"select * from imdb.movie where id = {movie_id}"
        lock.acquire()
        c.execute(stmt)
        lock.release()
        movie_page_res = c.fetchone()
        
        stmt = f"select * from imdb.review where movie_id = {movie_id} order by date desc"
        lock.acquire()
        c.execute(stmt)
        lock.release()
        reviews = c.fetchall()

        if current_user.is_authenticated:
            stmt = f"select * from imdb.vote where movie_id = {movie_id} and user_id = {current_user.id}"
            lock.acquire()
            c.execute(stmt)
            lock.release()
            votes = c.fetchall()
    else:
        if current_user.is_authenticated:
            if request.form.get('watchlist'):
                add_to_list("watchlist", current_user, movie_id)
            elif request.form.get('watched'):
                add_to_list("watched", current_user, movie_id)
        else:
            return redirect(url_for('auth.login'))
    return render_template("movie.html", user=current_user, movie=movie_page_res, reviews=reviews, votes=votes, is_admin=is_admin, filter=filter)