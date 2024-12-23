from flask import render_template

# 導入控制器
from app.controllers.customer_controller import customer_bp
from app.controllers.merchant_controller import merchant_bp
from app.controllers.delivery_controller import delivery_person_bp

# 定義 Blueprint 並註冊控制器
def register_routes(app):
    @app.route('/')
    def index():
        return render_template('choose_identity.html')
    # 註冊 Blueprint
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(merchant_bp, url_prefix='/merchants')
    app.register_blueprint(delivery_person_bp, url_prefix='/deliveries')


