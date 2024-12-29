from flask import Blueprint, request, jsonify, render_template
import app.models.delivery_person as DeliveryPerson
import app.models.order as Order

delivery_person_bp = Blueprint('delivery_person', __name__, url_prefix='/delivery_person')

@delivery_person_bp.route('/')
def index():
    return render_template('delivery/delivery_login.html')

@delivery_person_bp.route('/new')
def new():
    return render_template('delivery/delivery_register.html')

# 配送員註冊
@delivery_person_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        try:
            new_delivery_person = DeliveryPerson(
                name=data.get('name'),
                email=data.get('email'),
                password=data.get('password')  # 假設已處理密碼加密
            )
            # FIXME
            db.session.commit()
            return jsonify({'message': 'Delivery person registered successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return render_template('delivery/delivery_register.html')

# 查看分配的訂單
@delivery_person_bp.route('/assigned_orders', methods=['GET'])
def view_assigned_orders():
    delivery_person_id = request.args.get('delivery_person_id')
    try:
        # FIXME: Delievery person assignment
        orders = Order.get_orders_by_delivery_person(delivery_person_id=delivery_person_id, status='assigned').all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 接受訂單
@delivery_person_bp.route('/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    try:
        # FIXME: update_order_status(assigned)
        order = Order.update_order_status(order_id)
        if not order or order.status != 'assigned':
            return jsonify({'error': 'Order not found or already accepted'}), 404

        order.status = 'in_progress'
        # FIXME
        db.session.commit()
        return jsonify({'message': 'Order accepted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 查看配送歷史
@delivery_person_bp.route('/history', methods=['GET'])
def view_delivery_history():
    delivery_person_id = request.args.get('delivery_person_id')
    try:
        orders = Order.get_orders_by_delivery_person(delivery_person_id=delivery_person_id, status='delivered').all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 更新訂單狀態為已配送
@delivery_person_bp.route('/mark_delivered/<int:order_id>', methods=['POST'])
def mark_order_delivered(order_id):
    try:
        # FIXME: update_order_status(DONE)
        order = Order.update_order_status(order_id)
        if not order or order.status != 'in_progress':
            return jsonify({'error': 'Order not found or not in progress'}), 404

        order.status = 'delivered'
        # FIXME
        db.session.commit()
        return jsonify({'message': 'Order marked as delivered successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
