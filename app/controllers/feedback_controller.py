from flask import Blueprint, request, jsonify, render_template, session, flash, redirect
import app.models.feedback as Feedback
import app.models.order as Order

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

# 提交回饋
@feedback_bp.route('/submit', methods=['POST'])
def submit_feedback():
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    data = request.json
    try:
        # 確認訂單是否存在且已完成
        order = Order.get_order(data.get('order_id'))
        if not order or order.status != 'delivered':
            return jsonify({'error': 'Order not found or not delivered'}), 404

        # 新增回饋
        new_feedback = Feedback(
            order_id=data.get('order_id'),
            customer_id=data.get('customer_id'),
            rating=data.get('rating'),
            comment=data.get('comment', '')
        )
        # FIXME
        db.session.commit()
        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 查看指定訂單的回饋
@feedback_bp.route('/order/<int:order_id>', methods=['GET'])
def view_feedback_by_order(order_id):
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    try:
        # FIXME
        feedback = Feedback.query.filter_by(order_id=order_id).first()
        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404

        return jsonify(feedback.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 查看商家的所有回饋
@feedback_bp.route('/merchant/<int:merchant_id>', methods=['GET'])
def view_feedback_by_merchant(merchant_id):
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    try:
        # FIXME
        feedbacks = Feedback.query.filter_by(merchant_id=merchant_id).all()
        return jsonify([feedback.to_dict() for feedback in feedbacks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 刪除回饋 (僅限管理員或相關用戶)
@feedback_bp.route('/delete/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    if 'id' not in session:
        flash('請先登入！')
        return redirect('/')
    
    try:
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404
        # FIXME
        db.session.commit()
        return jsonify({'message': 'Feedback deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
