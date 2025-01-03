from flask import Blueprint, request, jsonify, render_template, redirect, session, flash
import app.models.merchant as Merchant
import app.models.menu_item as MenuItem
import app.models.order as Order

merchant_bp = Blueprint('merchant', __name__, url_prefix='/merchant')

@merchant_bp.route('/')
def index():
    return render_template('merchant/merchant_login.html')

@merchant_bp.route('/new')
def new():
    return render_template('merchant/merchant_register.html')

@merchant_bp.route('/newadd')
def newadd():
    merchant_id = session['id']
    return render_template('merchant/add_item.html', merchant_id=merchant_id)

# 商家註冊
@merchant_bp.route('/register', methods=['POST'])
def register():
    # 假設我們獲取表單資料
    name = request.form['name']
    password = request.form['password']
    location=request.form['location']
    contact_info = request.form['contact_info']
    # 進行用戶註冊邏輯，比如存儲用戶資料到資料庫
    if name and password and contact_info:
        Merchant.add_merchant( name,password,location, contact_info)
        # 例如將資料存入資料庫
        return redirect('/')
    return '註冊失敗'

@merchant_bp.route('/login', methods=['GET', 'POST'])
def login():
    name = request.form['username']
    password = request.form['password']

    # 透過 id 查詢用戶
    result, id = Merchant.login(name, password)
    if result:  # 直接比較明文密碼
        session['id'] = id  # 將用戶 ID 保存到 session
        flash('登入成功！')
        return redirect('menu')  # 登入成功，重定向到 merchant

    flash('登入失敗，請檢查您的帳號和密碼。')
    return redirect('/merchants/')  # 登入失敗，重定向到登入頁

# 查看菜單
@merchant_bp.route('/menu', methods=['GET'])
def view_menu():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    merchant_id = session['id']
    menu_items = MenuItem.get_menu_items_by_merchant(merchant_id=merchant_id)
    return render_template('merchant/manage_menu.html', menu_items=menu_items, merchant_id=merchant_id)

# 新增菜單項目
@merchant_bp.route('/menu/add', methods=['GET', 'POST'])
def add_menu_items(): 
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    name=request.form.get('name')
    price=request.form.get('price')
    description=request.form.get('description')
    merchant_id=session['id']
        
    MenuItem.add_menu_item(name=name, price=price, description=description, availability_status='1', merchant_id=merchant_id)
    flash('商品更新成功！')
    return redirect('/merchants/menu')

@merchant_bp.route('/menu/view', methods=['GET', 'POST'])
def view_menu_by_id():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    # 獲取商品詳細資訊
    menuitem_id=request.form['id']
    product = MenuItem.get_menu_item(menu_item_id=menuitem_id)
    return render_template('merchant/edit_item.html', item=product)

# 編輯菜單項目
@merchant_bp.route('/menu/edit', methods=['GET', 'POST'])
def edit_product():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    item_id = request.form.get('id')
    newname = request.form.get('newname')
    newdescription = request.form.get('newdescription')
    newprice = request.form.get('newprice')
    
    # 更新商品的資料
    MenuItem.update_menu_item(name=newname, price=newprice, description=newdescription, availability_status=1, id=item_id)
    flash('商品更新成功！')
    return redirect('/merchants/menu')

# 刪除菜單項目
@merchant_bp.route('/menu/delete', methods=['GET', 'POST'])
def delete_menu_item():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    item_id = request.form.get('id')
    MenuItem.delete_menu_item(menu_item_id=item_id)
    return redirect('/merchants/menu')
    
# 商家查看訂單列表
@merchant_bp.route('/orders', methods=['GET'])
def view_merchant_orders():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    merchant_id = session['id']
    orders = Order.get_orders_by_merchant(merchant_id=merchant_id)
    return render_template('merchant/order_list.html', data=orders, merchant_id=merchant_id)

@merchant_bp.route('/orders/accept', methods=['GET', 'POST'])
def accept_orders():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    merchant_id = session['id']
    order_id = request.form.get('order_id')
    Order.update_order_status(status='等待配送', id=order_id)
    orders = Order.get_orders_by_merchant(merchant_id=merchant_id)
    return render_template('merchant/order_list.html', data=orders, merchant_id=merchant_id)
