from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    ####### ASSETS ########
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


    ############# CONFIG #############
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wbbajeubxwdijf:42d9230539d6322698cb30380c5542d6549909ba71664a7dbb6f064923c0ff79@ec2-3-212-143-188.compute-1.amazonaws.com:5432/ddnpsj9vqfmh7u'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    ######### DB #################

    from models.models import db,student
    db.init_app(app)


    ############ LOGIN ##############
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return student.query.get(int(user_id))

    ###########ADDING ROUTES/BLUEPRINTS#############
    @app.route("/")
    def index():
        return render_template("index.html")
    
    # Forms
    from forms.auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from forms.checkout import checkout
    app.register_blueprint(checkout, url_prefix="/checkout")

    from forms.reserve import reserve
    app.register_blueprint(reserve, url_prefix="/reserve")

    # Views
    from views.admin import admin
    app.register_blueprint(admin, url_prefix="/admin")

    from views.main import main
    app.register_blueprint(main)

    return app