from app.controllers.customer_controller import customer_bp
from app.controllers.merchant_controller import merchant_bp

def register_routes(app):
    app.register_blueprint(customer_bp, url_prefix="/customer")
    app.register_blueprint(merchant_bp, url_prefix="/merchant")
