# 初始化 Flask 應用、配置檔案和 SQLAlchemy 資料庫。
from flask import Flask
from config.routes import register_routes

def create_app():
    app = Flask(__name__, static_folder='static',static_url_path='/')
    #set a secret key to hash cookies
    app.config['SECRET_KEY'] = '123TyU%^&'
    register_routes(app)

    return app
