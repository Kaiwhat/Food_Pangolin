# 初始化 Flask 應用、配置檔案和 SQLAlchemy 資料庫。
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.routes import register_routes

# 資料庫實例
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # 配置應用程式
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化資料庫
    db.init_app(app)

    # 註冊路由
    register_routes(app)

    return app
