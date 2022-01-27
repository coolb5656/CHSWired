from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    assets = Environment(app)

    bundles = {
        'js': Bundle(
            'js/lib/jquery-3.6.0.min.js',
            'js/scan.js',
            output='gen/app.js'),
        'css': Bundle(
            'css/style.css',
            'css/lib/bootstrap.css',
            output='gen/style.css'),
    }

    assets.register(bundles)

    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import student

    @login_manager.user_loader
    def load_user(user_id):
        return student.query.get(int(user_id))

    @app.route("/")
    def index():
        return render_template("index.html")

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # # blueprint for auth routes in our app
    # from .admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # blueprint for reserve routes in our app
    from .checkout import checkout as checkout_blueprint
    app.register_blueprint(checkout_blueprint, url_prefix='/checkout')

    # blueprint for reserve routes in our app
    from .reserve import reserve as reserve_blueprint
    app.register_blueprint(reserve_blueprint, url_prefix="/reservation")

    # blueprint for main parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.app = app
    return app