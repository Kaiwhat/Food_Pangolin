from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import app.models.customer as Customer
import app.models.order as Order
import app.models.menu_item as MenuItem
import app.models.merchant as Merchant
import app.models.order_item as OrderItem
import app.models.feedback as Feedback

# FIXME: WTF is db
from app import db  # SQLAlchemy 資料庫實例

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # FIXME: Change add_cistomer() parameter
        Customer.add_customer(name, email, password) 
        flash('註冊成功，請登入！')
        return redirect('/')  # 重定向到首頁
    return render_template('register.html')

# 登入功能
@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # 透過 email 查詢用戶
    user = Customer.get_user_by_email(email)
    if user and password == user['password']:  # 直接比較明文密碼
        session['id'] = user['id']  # 將用戶 ID 保存到 session
        flash('登入成功！')
        return redirect('/final_board')  # 登入成功，重定向到 final_board.html

    flash('登入失敗，請檢查您的電子郵件和密碼。')
    return redirect('/')  # 登入失敗，重定向到首頁

@customer_bp.route('/browse_menu', methods=['GET'])
def browse_menu():
    """顧客瀏覽菜單"""
    try:
        menu_items = MenuItem.get_menu_items_by_merchant()  # 從資料庫取得所有菜單項目
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
        
        # FIXME: What...?
        order = Order(customer_id=customer_id, status="pending")
        # FIXME
        db.session.add(order)
        # FIXME
        db.session.flush()  # 暫存以獲取 order.id

        # 添加訂單項目
        for item_id, quantity in zip(item_ids, quantities):
            # FIXME
            order_item = Order.add_item(order_id=order.id, menu_item_id=item_id, quantity=quantity)
            # FIXME
            db.session.add(order_item)
        # FIXME
        db.session.commit()  # 提交交易
        flash("訂單已成功提交！")
        return redirect(url_for('customer.browse_menu'))
    except Exception as e:
        # FIXME
        db.session.rollback()
        flash("提交訂單時出錯，請稍後再試。")
        return redirect(url_for('customer.browse_menu'))

@customer_bp.route('/order_history/<int:customer_id>', methods=['GET'])
def order_history(customer_id):
    """顧客查看訂單歷史"""
    try:
        orders = Order.get_orders_by_customer(customer_id=customer_id)
        return render_template('customer/order_history.html', orders=orders)
    except Exception as e:
        flash("無法加載訂單歷史，請稍後再試。")
        return render_template('customer/order_history.html', orders=[])

# 顯示顧客的訂單列表
@customer_bp.route('/customer/<int:customer_id>', methods=['GET'])
def view_customer_orders(customer_id):
    try:
        # FIXME: query.filter_by() ?
        orders = Order.query.filter_by(customer_id=customer_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

#全部商家
@customer_bp.route('/merchants', methods=['GET'])
def browse_merchants():
    merchants = Merchant.query.all()
    return render_template('customer/browse_merchant.html', merchants=merchants)

@customer_bp.route('/menu/<int:merchant_id>', methods=['GET'])
def browse_menu(merchant_id):
    # FIXME: query.filter_by() ?
    menu_items = MenuItem.query.filter_by(merchant_id=merchant_id).all()
    return render_template('customer/browse_menu.html', menu_items=menu_items, merchant_id=merchant_id)

@customer_bp.route('/order', methods=['POST'])
def place_order():
    data = request.form
    order = Order(customer_id=data.get('customer_id'), merchant_id=data.get('merchant_id'))
    # FIXME
    db.session.add(order)
    # FIXME
    db.session.flush()  # Get the generated order ID

    for item_id, quantity in data.items():
        if item_id.startswith('item_'):
            menu_item_id = int(item_id.split('_')[1])
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item_id,
                quantity=int(quantity)
            )
            # FIXME
            db.session.add(order_item)
    # FIXME
    db.session.commit()
    return redirect(url_for('customer.order_status', order_id=order.id))

@customer_bp.route('/order_status/<int:order_id>', methods=['GET'])
def order_status(order_id):
    order = Order.get_order_items(order_id)
    return render_template('customer/order_status.html', order=order)

@customer_bp.route('/feedback/<int:order_id>', methods=['GET', 'POST'])
def grade_order(order_id):
    if request.method == 'POST':
        data = request.form
        feedback = Feedback(
            order_id=order_id,
            rating=data.get('rating'),
            comments=data.get('comments')
        )
        # FIXME
        db.session.add(feedback)
        # FIXME
        db.session.commit()
        return redirect(url_for('customer.browse_merchants'))
    return render_template('customer/grade_order.html', order_id=order_id)

# FIXME:
@customer_bp.route('/history/<int:customer_id>', methods=['GET'])
def customer_history(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return render_template('customer/customer_history.html', orders=orders)
