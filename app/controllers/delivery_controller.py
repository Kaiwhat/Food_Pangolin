from flask import Blueprint, request, jsonify, render_template, session, redirect, flash,url_for
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
@delivery_person_bp.route('/register', methods=['POST'])
def register():
    # 假設我們獲取表單資料
    name = request.form['name']
    password = request.form['password']
    vehicle=request.form['vehicle_info']
    contact_info = request.form['contact_info']
    # 進行用戶註冊邏輯，比如存儲用戶資料到資料庫
    if name and password and contact_info:
        DeliveryPerson.add_delivery_person( name,password,vehicle, contact_info)
        # 例如將資料存入資料庫
        return redirect('/')
    return '註冊失敗'

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
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    DeliveryPerson_id = session['id']
    order = Order.get_orders_by_delivery(DeliveryPerson_id)
    print("Latest orders:", order)
    
    return render_template('delivery/assigned_order.html', data=order, DeliveryPerson_id=DeliveryPerson_id)

# 接受訂單
@delivery_person_bp.route('/accept_order', methods=['POST'])
def accept_order():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    # 從表單獲取 delivery_person_id 和 order_id
    DeliveryPerson_id = session['id']
    order_id = request.form.get('id')  # 使用 request.form.get() 來獲取 id
    Order.delivery_add_order(DeliveryPerson_id, order_id)  # 呼叫函數來處理接單
    return redirect('assigned_orders')


# 查看配送歷史
@delivery_person_bp.route('/history', methods=['GET'])
def view_delivery_history():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    DeliveryPerson_id = session['id']
    history = Order.get_orders_by_delivery_person(DeliveryPerson_id)
    
    return render_template('delivery/delivery_history.html', data=history, DeliveryPerson_id=DeliveryPerson_id)

# 更新訂單狀態為已配送
@delivery_person_bp.route('/mark_order_delivered', methods=['POST'])
def mark_order_delivered():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    DeliveryPerson_id = session['id']
    order_id = request.form.get('order_id')
    if order_id:
        Order.update_order_status(status='已送達', id=order_id)
        Order.add_total_pay(DeliveryPerson_id,order_id)
    return redirect('assigned_orders')

# 檢索所有 "等待配送" 的訂單
@delivery_person_bp.route('/pending_orders')
def view_pending_orders():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    # 假設有一個方法在 Order 模型中檢索等待配送的訂單
    pending_orders = Order.All_pending_orders()
    return render_template('delivery/select_All_null_take.html', pending_orders=pending_orders)

#確認取貨
@delivery_person_bp.route('/mark_order_pick', methods=['POST'])
def mark_order_pick():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    order_id = request.form.get('order_id')
    if order_id:
        Order.update_order_status_pick(order_id)
    return redirect('assigned_orders')