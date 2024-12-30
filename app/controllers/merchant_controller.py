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
@merchant_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        try:
            new_merchant = Merchant(
                name=data.get('name'),
                email=data.get('email'),
                password=data.get('password')  # 假設已處理密碼加密
            )
            # FIXME
            db.session.commit()
            return jsonify({'message': 'Merchant registered successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return render_template('merchant/merchant_register.html')

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
    merchant_id = session['id']
    menu_items = MenuItem.get_menu_items_by_merchant(merchant_id=merchant_id)
    return render_template('merchant/manage_menu.html', menu_items=menu_items, merchant_id=merchant_id)

# 新增菜單項目
@merchant_bp.route('/menu/add', methods=['GET', 'POST'])
def add_menu_items(): 
    name=request.form.get('name')
    price=request.form.get('price')
    description=request.form.get('description')
    merchant_id=session['id']
        
    Merchant.add_menu_item(name=name, price=price, description=description, availability_status='1', merchant_id=merchant_id)
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
    item_id = request.form.get('id')
    Merchant.delete_menu_item(menu_item_id=item_id)
    return redirect('/merchants/menu')
    
# 商家查看訂單列表
@merchant_bp.route('/orders', methods=['GET'])
def view_merchant_orders():
    merchant_id = session['id']
    orders = Order.get_orders_by_merchant(merchant_id=merchant_id)
    return render_template('merchant/order_list.html', data=orders, merchant_id=merchant_id)

@merchant_bp.route('/orders/complete', methods=['GET'])
def complete_orders():
    merchant_id = session['id']
    item_id = request.form.get('item_id')
    order_id = request.form.get('order_id')
    orders = Order.get_orders_by_merchant(merchant_id=merchant_id)
    return render_template('merchant/order_list.html', data=orders, merchant_id=merchant_id)

