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
    try:
        # FIXME
        menu_items = MenuItem.get_menu_items_by_merchant(merchant_id=merchant_id)
        return render_template('merchant/manage_menu.html', menu_items=menu_items, merchant_id=merchant_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 新增菜單項目
@merchant_bp.route('/menu/add', methods=['POST'])
def add_menu_items():
    try:
        
        name=request.form.get('name'),
        price=request.form.get('price'),
        description=request.form.get('description'),
        merchant_id=session['id']
        
        new_item = Merchant.add_menu_item(newname=name, newprice=price, newdescription=description, availability_status=1, merchant_id=merchant_id)
        return jsonify({'message': 'Menu item added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 編輯菜單項目
@merchant_bp.route('/menu/edit/<int:item_id>', methods=['POST','GET'])
def edit_menu_item(item_id):
    
    try:
        # FIXME
        item = MenuItem.update_menu_item(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        name=request.form.get('name'),
        price=request.form.get('price'),
        description=request.form.get('description'),
        merchant_id=session['id']
        
        # FIXME
        edit_item = Merchant.update_menu_item(newname=name, newprice=price, newdescription=description, availability_status=1, merchant_id=merchant_id)
        return jsonify({'message': 'Menu item updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 刪除菜單項目
@merchant_bp.route('/menu/delete/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    try:
        item = MenuItem.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        # FIXME
        db.session.commit()
        return jsonify({'message': 'Menu item deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# 商家查看訂單列表
@merchant_bp.route('/merchant/<int:merchant_id>', methods=['GET'])
def view_merchant_orders(merchant_id):
    try:
        orders = Order.get_orders_by_merchant(merchant_id=merchant_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
