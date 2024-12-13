from flask import Blueprint, request, jsonify, render_template
from app.models.merchant import Merchant
from app.models.menu_item import MenuItem
from app.models import db

merchant_bp = Blueprint('merchant', __name__, url_prefix='/merchant')

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
            db.session.add(new_merchant)
            db.session.commit()
            return jsonify({'message': 'Merchant registered successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    return render_template('merchant/merchant_register.html')

# 查看菜單
@merchant_bp.route('/menu', methods=['GET'])
def view_menu():
    merchant_id = request.args.get('merchant_id')
    try:
        menu_items = MenuItem.query.filter_by(merchant_id=merchant_id).all()
        return jsonify([item.to_dict() for item in menu_items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 新增菜單項目
@merchant_bp.route('/menu/add', methods=['POST'])
def add_menu_item():
    data = request.json
    try:
        new_item = MenuItem(
            name=data.get('name'),
            price=data.get('price'),
            description=data.get('description'),
            merchant_id=data.get('merchant_id')
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Menu item added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# 編輯菜單項目
@merchant_bp.route('/menu/edit/<int:item_id>', methods=['PUT'])
def edit_menu_item(item_id):
    data = request.json
    try:
        item = MenuItem.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        item.name = data.get('name', item.name)
        item.price = data.get('price', item.price)
        item.description = data.get('description', item.description)

        db.session.commit()
        return jsonify({'message': 'Menu item updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# 刪除菜單項目
@merchant_bp.route('/menu/delete/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    try:
        item = MenuItem.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Menu item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
# 商家查看訂單列表
@merchant_bp.route('/merchant/<int:merchant_id>', methods=['GET'])
def view_merchant_orders(merchant_id):
    try:
        orders = Order.query.filter_by(merchant_id=merchant_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
