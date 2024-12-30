from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import app.models.customer as Customer
import app.models.order as Order
import app.models.menu_item as MenuItem
import app.models.merchant as Merchant
import app.models.order_item as OrderItem
import app.models.feedback as Feedback
import app.models.cart as Cart
import random

#
customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/')
def index():
    return render_template('customer/customer_login.html')

@customer_bp.route('/new')
def new():
    return render_template('customer/customer_register.html')

# 顧客註冊
@customer_bp.route('/register', methods=['POST'])
def register():
    # 假設我們獲取表單資料
    name = request.form['name']
    password = request.form['password']
    address=request.form['address']
    contact_info = request.form['contact_info']
    # 進行用戶註冊邏輯，比如存儲用戶資料到資料庫
    if name and password and contact_info:
        Customer.add_customer( name,password,address, contact_info)
        # 例如將資料存入資料庫
        return redirect('/')
    return '註冊失敗'

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

# 顯示顧客的訂單列表
@customer_bp.route('/customer/<int:customer_id>', methods=['GET'])
def view_customer_orders(customer_id):
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    try:
        # FIXME: query.filter_by() ?
        orders = Order.query.filter_by(customer_id=customer_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

#全部商家
@customer_bp.route('/merchants', methods=['GET'])
def browse_merchants():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    merchants = Merchant.get_all_merchant()
    customer_id = session['id']
    return render_template('customer/browse_merchant.html', items=merchants, customer_id=customer_id)

@customer_bp.route('/menu', methods=['GET'])
def browse_menu():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    merchant_id = request.args.get('merchant_id', type=int)
    session['merchant_id']=merchant_id
    menu_items = Merchant.get_menu_items(merchant_id=merchant_id)
    return render_template('customer/browse_menu.html', items=menu_items, merchant_id=merchant_id)


@customer_bp.route('/order_status/<int:order_id>', methods=['GET'])
def order_status(order_id):
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    order = Order.get_order_items(order_id)
    return render_template('customer/order_status.html', order=order)

@customer_bp.route('/feedback/<int:order_id>', methods=['GET', 'POST'])
def grade_order(order_id):
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
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

# 查看配送歷史
@customer_bp.route('/history', methods=['GET'])
def view_customer_history():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    customer_id = session['id']
    history = Order.get_orders_by_customer(customer_id)
    return render_template('customer/customer_history.html', orders=history, customer_id=customer_id)



@customer_bp.route('/cart', methods=['GET'])
def view_cart():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    """檢視購物車內容"""
    customer_id = session['id']
    cart_items = Cart.view_cart(customer_id=customer_id)
    return render_template('customer/place_order.html', items=cart_items)

@customer_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
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
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    """移除購物車中的商品"""
    customer_id = session['id']
    menuitem_id = request.form['id']

    cart_item = Cart.remove_from_cart(customer_id=customer_id, menuitem_id=menuitem_id)
    return redirect('/customers/cart')

@customer_bp.route('/cart/place_order', methods=['POST'])
def place_order():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    """確定購買，轉換為訂單"""
    customer_id = session['id']
    delivery_address = request.form.get('address')

    # 獲取購物車內容
    cart_items = Cart.view_cart(customer_id=customer_id)
    if not cart_items:
        flash('購物車為空，無法提交訂單')
        return redirect(url_for('/customers/cart'))

    # 計算總金額
    total_price = sum(item['total_price'] for item in cart_items)

    # 插入訂單資料
    order_id = Order.add_order(customer_id=customer_id, delivery_person_id='999', status=0, delivery_address=delivery_address, total_price=total_price, created_at=0)

    # 插入訂單項目
    # 清空購物車
    for item in cart_items:

        # 新增訂單項目
        Order.add_order_item(
            order_id=order_id,
            menu_item_id=item['menuitem_id'],  # 傳遞單一值
            quantity=item['quantity'],
            price=int(item['total_price'])
        )

        # 從購物車中移除項目
        Cart.remove_from_cart(customer_id=customer_id, menuitem_id=item['menuitem_id'])

    flash(f'訂單已成功提交，總金額：{total_price} 元')
    return redirect('/customers/cart')
