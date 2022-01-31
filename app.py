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


    @app.route("/")
    def index():
        return render_template("index.html")

    return app