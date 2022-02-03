from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    app.config["DEBUG"] = True

    # Upload folder
    UPLOAD_FOLDER = 'static/upload'
    app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

    ####### ASSETS ########
    assets = Environment(app)

    bundles = {
        'js': Bundle(
            'js/app.js',
            output='gen/app.js'),
        'adminjs': Bundle(
            'js/admin.js',
            output='gen/scan.js'),
        'scanjs': Bundle(
            'js/scan.js',
            output='gen/scan.js'),
        'css': Bundle(
            'css/style.css',
            output='gen/style.css'),
    }

    assets.register(bundles)


    ############# CONFIG #############
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
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