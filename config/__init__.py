from flask import Flask

def create_app():
    """創建並配置 Flask 應用程式"""
    app = Flask(__name__)

    # 設定應用程式配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    # 註冊 Blueprint
    from app.controllers.customer_controller import customer_bp
    app.register_blueprint(customer_bp)

    from app.controllers.merchant_controller import merchant_bp
    app.register_blueprint(merchant_bp)

    from app.controllers.delivery_controller import delivery_person_bp
    app.register_blueprint(delivery_person_bp)

    return app
