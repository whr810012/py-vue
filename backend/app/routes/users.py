from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.registration import Registration
from app.models.activity import Activity
from sqlalchemy import func

users_bp = Blueprint('users', __name__)

@users_bp.route('/my-registrations', methods=['GET'])
@jwt_required()
def get_my_registrations():
    """获取我的报名记录"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        query = Registration.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter(Registration.status == status)
        
        # 按报名时间倒序排列
        query = query.order_by(Registration.registration_time.desc())
        
        # 分页
        registrations = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # 获取活动详情
        result = []
        for reg in registrations.items:
            reg_dict = reg.to_dict()
            activity = Activity.query.get(reg.activity_id)
            if activity:
                reg_dict['activity'] = activity.to_dict()
            result.append(reg_dict)
        
        return jsonify({
            'registrations': result,
            'total': registrations.total,
            'pages': registrations.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/my-activities', methods=['GET'])
@jwt_required()
def get_my_activities():
    """获取我创建的活动"""
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Activity.query.filter_by(created_by=user_id)
        query = query.order_by(Activity.created_at.desc())
        
        # 分页
        activities = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'activities': [activity.to_dict() for activity in activities.items],
            'total': activities.total,
            'pages': activities.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_user_statistics():
    """获取用户统计信息"""
    try:
        user_id = get_jwt_identity()
        
        # 总报名次数
        total_registrations = Registration.query.filter_by(user_id=user_id).count()
        
        # 已完成活动数
        completed_activities = Registration.query.filter_by(
            user_id=user_id, status='completed'
        ).count()
        
        # 已签到活动数
        checked_in_activities = Registration.query.filter_by(
            user_id=user_id, status='checked_in'
        ).count()
        
        # 取消的活动数
        cancelled_activities = Registration.query.filter_by(
            user_id=user_id, status='cancelled'
        ).count()
        
        # 获取用户信息（包含志愿时长）
        user = User.query.get(user_id)
        
        # 创建的活动数
        created_activities = Activity.query.filter_by(created_by=user_id).count()
        
        return jsonify({
            'total_registrations': total_registrations,
            'completed_activities': completed_activities,
            'checked_in_activities': checked_in_activities,
            'cancelled_activities': cancelled_activities,
            'volunteer_hours': user.volunteer_hours if user else 0,
            'created_activities': created_activities
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/check-in/<int:registration_id>', methods=['POST'])
@jwt_required()
def check_in(registration_id):
    """活动签到"""
    try:
        user_id = get_jwt_identity()
        
        registration = Registration.query.filter_by(
            id=registration_id, user_id=user_id
        ).first()
        
        if not registration:
            return jsonify({'error': 'Registration not found'}), 404
        
        if registration.check_in():
            db.session.commit()
            return jsonify({
                'message': 'Check-in successful',
                'registration': registration.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Cannot check in at this time'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/complete/<int:registration_id>', methods=['POST'])
@jwt_required()
def complete_activity(registration_id):
    """完成活动"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        registration = Registration.query.filter_by(
            id=registration_id, user_id=user_id
        ).first()
        
        if not registration:
            return jsonify({'error': 'Registration not found'}), 404
        
        rating = data.get('rating')
        feedback = data.get('feedback')
        
        if registration.complete(rating=rating, feedback=feedback):
            # 更新用户志愿时长
            activity = Activity.query.get(registration.activity_id)
            if activity and activity.volunteer_hours > 0:
                user = User.query.get(user_id)
                if user:
                    user.volunteer_hours += activity.volunteer_hours
            
            db.session.commit()
            return jsonify({
                'message': 'Activity completed successfully',
                'registration': registration.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Cannot complete activity at this time'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500