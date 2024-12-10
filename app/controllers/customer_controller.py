from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.customer import Customer
from app.models.order import Order
from app.models.menu_item import MenuItem
from app import db  # SQLAlchemy 資料庫實例

# 定義 Blueprint
customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/browse_menu', methods=['GET'])
def browse_menu():
    """顧客瀏覽菜單"""
    try:
        menu_items = MenuItem.query.all()  # 從資料庫取得所有菜單項目
        return render_template('customer/browse_menu.html', menu_items=menu_items)
    except Exception as e:
        flash("無法加載菜單，請稍後再試。")
        return render_template('customer/browse_menu.html', menu_items=[])

@customer_bp.route('/place_order', methods=['POST'])
def place_order():
    """顧客下訂單"""
    try:
        customer_id = request.form.get('customer_id')  # 從前端表單接收顧客 ID
        item_ids = request.form.getlist('item_ids')    # 接收選中的菜單項目 ID 列表
        quantities = request.form.getlist('quantities')  # 接收數量列表
        
        # 創建訂單實例
        order = Order(customer_id=customer_id, status="pending")
        db.session.add(order)
        db.session.flush()  # 暫存以獲取 order.id

        # 添加訂單項目
        for item_id, quantity in zip(item_ids, quantities):
            order_item = Order.add_item(order_id=order.id, menu_item_id=item_id, quantity=quantity)
            db.session.add(order_item)
        
        db.session.commit()  # 提交交易
        flash("訂單已成功提交！")
        return redirect(url_for('customer.browse_menu'))
    except Exception as e:
        db.session.rollback()
        flash("提交訂單時出錯，請稍後再試。")
        return redirect(url_for('customer.browse_menu'))

@customer_bp.route('/order_history/<int:customer_id>', methods=['GET'])
def order_history(customer_id):
    """顧客查看訂單歷史"""
    try:
        orders = Order.query.filter_by(customer_id=customer_id).all()
        return render_template('customer/order_history.html', orders=orders)
    except Exception as e:
        flash("無法加載訂單歷史，請稍後再試。")
        return render_template('customer/order_history.html', orders=[])
