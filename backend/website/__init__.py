from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
database = "mysql+pymysql://guest@123.60.47.86:3306/imdb" # mysql://user:password@ip:port/database

engine = create_engine(database)
connection = engine.raw_connection()
c = connection.cursor()

app = None

def create_app():
    global app
    frontend_dir = path.dirname(path.dirname(path.abspath(path.dirname(__file__))))
    frontend_dir = path.join(frontend_dir, 'frontend')
    templates_dir = path.join(frontend_dir, 'templates')
    static_dir = path.join(frontend_dir, 'static')
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    app.config["SESSION_PERMANENT"] = False
    app.config['SECRET_KEY'] = '08df54d0d2s359sdffdgvbm'
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['UPLOAD_FOLDER'] = static_dir + '/images/'
    db.init_app(app)

    from .auth import auth
    from .models import User, Admin, Movie, Watchlist, Review

    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if int(id) == 99999:
            return Admin.query.get(int(id))
        return User.query.get(int(id))

    return app