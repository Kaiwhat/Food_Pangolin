from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import app.models.customer as Customer
import app.models.order as Order
import app.models.menu_item as MenuItem
import app.models.merchant as Merchant
import app.models.order_item as OrderItem
import app.models.feedback as Feedback
import app.models.cart as Cart


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
        id = None
        username = request.form['username']
        password = request.form['password']
        address = None
        contact_info = None

        # FIXME: Change add_customer() parameter
        Customer.add_customer(id, name, contact_info, address, password) 
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
    session['merchant_id']=merchant_id
    menu_items = Merchant.get_menu_items(merchant_id=merchant_id)
    return render_template('customer/browse_menu.html', items=menu_items, merchant_id=merchant_id)


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



@customer_bp.route('/cart', methods=['GET'])
def view_cart():
    """檢視購物車內容"""
    customer_id = session['id']
    cart_items = Cart.view_cart(customer_id=customer_id)
    return render_template('customer/place_order.html', items=cart_items)

@customer_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """將商品加入購物車"""
    customer_id = session['id']
    merchant_id = session['merchant_id']
    menuitem_id = request.form['id']
    quantity = 1

    cart_item = Cart.add_to_cart(customer_id=customer_id, menuitem_id=menuitem_id, quantity=quantity)
    menu_items = Merchant.get_menu_items(merchant_id=merchant_id)
    flash('商品新增成功！')
    return render_template('customer/browse_menu.html', items=menu_items, merchant_id=merchant_id)
   

@customer_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    """移除購物車中的商品"""
    customer_id = session['id']
    menuitem_id = request.form['id']

    cart_item = Cart.remove_from_cart(customer_id=customer_id, menuitem_id=menuitem_id)
    return redirect('/customers/cart')

@customer_bp.route('/cart/place_order', methods=['POST'])
def place_order():
    """確定購買，轉換為訂單"""
    customer_id = session['id']

    # 模擬轉換購物車為訂單邏輯
    cart_items = Cart.view_cart(customer_id=customer_id)
    if not cart_items:
        flash('Cart is empty')

    # 清空購物車並生成訂單（詳細實現略）
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()
    return jsonify({"message": "Order placed successfully"})
