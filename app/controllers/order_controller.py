from flask import Blueprint, request, jsonify, render_template
import app.models.order as Order
import app.models.order_item as OrderItem
import app.models.menu_item as MenuItem


order_bp = Blueprint('order', __name__, url_prefix='/order')



# 顧客下訂單(跟customercontroller)
@order_bp.route('/place', methods=['POST'])
def place_order():
    data = request.json
    try:
        # 新建訂單(訂單基底)
        new_order = Order(
            customer_id=data.get('customer_id'),
            merchant_id=data.get('merchant_id'),
            status='placed',
            total_price=0  # 初始為 0，稍後計算總價
        )

        # 新建訂單項目(新增訂單內的項目)
        total_price = 0
        for item in data.get('items', []):
            # FIXME
            menu_item = MenuItem.query.get(item['menu_item_id'])
            if not menu_item:
                raise Exception(f"Menu item {item['menu_item_id']} not found")

            order_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=menu_item.id,
                quantity=item['quantity'],
                price=menu_item.price * item['quantity']
            )
            total_price += order_item.price

        # 更新訂單總價
        new_order.total_price = total_price
        # FIXME
        db.session.commit()
        return jsonify({'message': 'Order placed successfully', 'order_id': new_order.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400



# 更新訂單狀態
@order_bp.route('/update_status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    try:
        # FIXME
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        order.status = data.get('status', order.status)
        # FIXME
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 查看訂單詳細資訊
@order_bp.route('/details/<int:order_id>', methods=['GET'])
def view_order_details(order_id):
    try:
        # FIXME
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        # FIXME
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        return jsonify({
            'order': order.to_dict(),
            'items': [item.to_dict() for item in order_items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
