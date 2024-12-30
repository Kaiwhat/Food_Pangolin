from flask import render_template, session, flash, redirect

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

    @app.route('/logout')
    def logout():
        session.pop('id', None)  # 刪除 session 中的用戶 ID
        flash('您已成功登出！')
        return redirect('/')  # 重定向到首頁