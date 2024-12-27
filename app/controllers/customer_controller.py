from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import app.models.customer as Customer
import app.models.order as Order
import app.models.menu_item as MenuItem
import app.models.merchant as Merchant
import app.models.order_item as OrderItem
import app.models.feedback as Feedback

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/')
def index():
    return render_template('customer/customer_login.html')

@customer_bp.route('/new')
def new():
    return render_template('customer/customer_register.html')

@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        password = request.form['password']
        address = request.form['address']
        
        # FIXME: Change add_customer() parameter
        Customer.add_customer(name, id, address) 
        flash('註冊成功，請登入！')
        return redirect('/customers/')  # 重定向到首頁
    return render_template('customer/customer_register.html')

# 登入功能
@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    name = request.form['username']
    password = request.form['password']

    # 透過 id 查詢用戶
    result, id = Customer.login(name, password)
    if result:  # 直接比較明文密碼
        session['id'] = id  # 將用戶 ID 保存到 session
        flash('登入成功！')
        return redirect('merchants')  # 登入成功，重定向到 merchant

    flash('登入失敗，請檢查您的帳號和密碼。')
    return redirect('/customers/')  # 登入失敗，重定向到登入頁

@customer_bp.route('/place_order', methods=['POST'])
def place_order():
    """顧客下訂單"""
    try:
        customer_id = request.form.get('customer_id')  # 從前端表單接收顧客 ID
        item_ids = request.form.getlist('item_ids')    # 接收選中的菜單項目 ID 列表
        quantities = request.form.getlist('quantities')  # 接收數量列表
        
        # FIXME: What...?
        order = Order(customer_id=customer_id, status="pending")

        # 添加訂單項目
        for item_id, quantity in zip(item_ids, quantities):
            # FIXME
            order_item = Order.add_item(order_id=order.id, menu_item_id=item_id, quantity=quantity)
        # FIXME
        db.session.commit()  # 提交交易
        flash("訂單已成功提交！")
        return redirect(url_for('customer/customer.browse_menu'))
    except Exception as e:
        flash("提交訂單時出錯，請稍後再試。")
        return redirect(url_for('customer/customer.browse_menu'))

# FIXME
@customer_bp.route('/order_history/<int:customer_id>', methods=['GET'])
def order_history(customer_id):
    """顧客查看訂單歷史"""
    try:
        orders = Order.get_orders_by_customer(customer_id=customer_id)
        return render_template('customer/order_history.html', orders=orders)
    except Exception as e:
        flash("無法加載訂單歷史，請稍後再試。")
        return render_template('customer/customer_history.html', orders=[])

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
    merchants = Merchant.get_all_merchant()
    customer_id = session['id']
    return render_template('customer/browse_merchant.html', items=merchants, customer_id=customer_id)

@customer_bp.route('/menu', methods=['GET'])
def browse_menu():
    merchant_id = request.args.get('merchant_id', type=int)
    menu_items = Merchant.get_menu_items(merchant_id=merchant_id)
    return render_template('customer/browse_menu.html', items=menu_items)


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
        db.session.commit()
        return redirect(url_for('customer.browse_merchants'))
    return render_template('customer/grade_order.html', order_id=order_id)

# FIXME:
@customer_bp.route('/history/<int:customer_id>', methods=['GET'])
def customer_history(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return render_template('customer/customer_history.html', orders=orders)
