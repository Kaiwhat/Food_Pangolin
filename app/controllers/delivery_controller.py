from flask import Blueprint, request, jsonify, render_template, session, redirect, flash
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

# 登入功能
@delivery_person_bp.route('/login', methods=['GET', 'POST'])
def login():
    name = request.form['username']
    password = request.form['password']

    # 透過 id 查詢用戶
    result, id = DeliveryPerson.login(name, password)
    if result:  # 直接比較明文密碼
        session['id'] = id  # 將用戶 ID 保存到 session
        flash('登入成功！')
        return redirect('assigned_orders')  # 登入成功，重定向到 merchant

    flash('登入失敗，請檢查您的帳號和密碼。')
    return redirect('/deliveries/')  # 登入失敗，重定向到登入頁

# 查看分配的訂單
@delivery_person_bp.route('/assigned_orders', methods=['GET'])
def view_assigned_orders():
    DeliveryPerson_id = session['id']
    order = DeliveryPerson.get_orders_by_delivery_person(DeliveryPerson_id)
    
    return render_template('delivery/assigned_order.html', data=order, DeliveryPerson_id=DeliveryPerson_id)

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
    DeliveryPerson_id = session['id']
    history = Order.get_orders_by_delivery_person(DeliveryPerson_id)
    
    return render_template('delivery/delivery_history.html', data=history, DeliveryPerson_id=DeliveryPerson_id)

# 更新訂單狀態為已配送
@delivery_person_bp.route('/mark_order_delivered', methods=['POST'])
def mark_order_delivered():
    order_id = request.form.get('order_id')
    if order_id:
        Order.update_order_status(order_id)
    return redirect('assigned_orders')

# 檢索所有 "等待配送" 的訂單
@delivery_person_bp.route('/pending_orders')
def view_pending_orders():
    # 假設有一個方法在 Order 模型中檢索等待配送的訂單
    pending_orders = Order.All_pending_orders()
    return render_template('delivery/select_All_null_take.html', pending_orders=pending_orders)


