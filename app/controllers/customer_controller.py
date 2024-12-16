from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.customer import Customer
from app.models.order import Order
from app.models.menu_item import MenuItem
from app import db  # SQLAlchemy 資料庫實例

# 定義 Blueprint
customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

# 註冊功能
@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  #雜湊密碼
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

# 登入功能
@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect('/auctions')
        else:
            return "登入失敗，請檢查使用者名稱或密碼"
    return render_template('login.html')

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

# 顯示顧客的訂單列表
@customer_bp.route('/customer/<int:customer_id>', methods=['GET'])
def view_customer_orders(customer_id):
    try:
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
    menu_items = MenuItem.query.filter_by(merchant_id=merchant_id).all()
    return render_template('customer/browse_menu.html', menu_items=menu_items, merchant_id=merchant_id)

@customer_bp.route('/order', methods=['POST'])
def place_order():
    data = request.form
    order = Order(customer_id=data.get('customer_id'), merchant_id=data.get('merchant_id'))
    db.session.add(order)
    db.session.flush()  # Get the generated order ID

    for item_id, quantity in data.items():
        if item_id.startswith('item_'):
            menu_item_id = int(item_id.split('_')[1])
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item_id,
                quantity=int(quantity)
            )
            db.session.add(order_item)

    db.session.commit()
    return redirect(url_for('customer.order_status', order_id=order.id))

@customer_bp.route('/order_status/<int:order_id>', methods=['GET'])
def order_status(order_id):
    order = Order.query.get(order_id)
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
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('customer.browse_merchants'))
    return render_template('customer/grade_order.html', order_id=order_id)

@customer_bp.route('/history/<int:customer_id>', methods=['GET'])
def customer_history(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return render_template('customer/customer_history.html', orders=orders)
