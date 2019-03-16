# -*- code:utf-8 -*-
from flask import Flask
from werkzeug.routing import  BaseConverter
from os import path
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user
from flask_gravatar import Gravatar
from flask_babel import Babel,gettext as _
from config import config

class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex=items[0]

basedir = path.abspath(path.dirname(__file__))


# manager = Manager(app)
babel = Babel()
bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view = 'auth.login'



nav.register_element('top',Navbar('微信管理',
                                  View(u'首页','main.index'),
                                  View(u'关于','main.about'),
                                  View(u'服务','main.services'),
                                  View(u'项目','main.projects')))

def create_app(config_name='default'):
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.config.from_object(config[config_name])
    #app.config.from_pyfile('babel.cfg')
    #app.secret_key = 'hard to guess string'
    # app.config['BABEL_DEFAULT_LOCALE']='zh'
    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    #     'sqlite:///' + path.join(basedir, 'data.sqlite')
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    #nav.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    Gravatar(app, size=64)
    babel.init_app(app)

    from .auth import auth  as auth_blueprint
    from .main import main  as main_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    app.register_blueprint(main_blueprint,static_folder='static')

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    # @babel.localeselector
    # def get_locale():
    #     return current_user.locale


    return app





