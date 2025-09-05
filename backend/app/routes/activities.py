from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.activity import Activity
from app.models.registration import Registration
from app.models.user import User
from datetime import datetime
from sqlalchemy import or_

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/', methods=['GET'])
def get_activities():
    """获取活动列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        status = request.args.get('status', 'active')
        search = request.args.get('search')
        
        query = Activity.query
        
        # 筛选条件
        if category:
            query = query.filter(Activity.category == category)
        if status:
            query = query.filter(Activity.status == status)
        if search:
            query = query.filter(or_(
                Activity.title.contains(search),
                Activity.description.contains(search)
            ))
        
        # 按创建时间倒序排列
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

@activities_bp.route('/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    """获取单个活动详情"""
    try:
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        return jsonify({'activity': activity.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/', methods=['POST'])
@jwt_required()
def create_activity():
    """创建新活动"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['title', 'description', 'location', 'start_time', 'end_time']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # 解析时间
        try:
            start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid datetime format'}), 400
        
        if start_time >= end_time:
            return jsonify({'error': 'Start time must be before end time'}), 400
        
        # 创建活动
        activity = Activity(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            start_time=start_time,
            end_time=end_time,
            max_participants=data.get('max_participants', 50),
            category=data.get('category', ''),
            volunteer_hours=data.get('volunteer_hours', 0.0),
            requirements=data.get('requirements', ''),
            contact_person=data.get('contact_person', ''),
            contact_phone=data.get('contact_phone', ''),
            image_url=data.get('image_url', ''),
            created_by=user_id
        )
        
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'message': 'Activity created successfully',
            'activity': activity.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>/register', methods=['POST'])
@jwt_required()
def register_activity(activity_id):
    """报名参加活动"""
    try:
        user_id = get_jwt_identity()
        
        # 检查活动是否存在
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # 检查活动状态
        if not activity.is_active:
            return jsonify({'error': 'Activity is not available for registration'}), 400
        
        # 检查是否已满员
        if activity.is_full:
            return jsonify({'error': 'Activity is full'}), 400
        
        # 检查是否已报名
        existing_registration = Registration.query.filter_by(
            user_id=user_id, activity_id=activity_id
        ).first()
        
        if existing_registration:
            return jsonify({'error': 'Already registered for this activity'}), 400
        
        # 创建报名记录
        registration = Registration(
            user_id=user_id,
            activity_id=activity_id,
            notes=request.get_json().get('notes', '') if request.get_json() else ''
        )
        
        # 更新活动参与人数
        activity.current_participants += 1
        
        db.session.add(registration)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'registration': registration.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/<int:activity_id>/unregister', methods=['DELETE'])
@jwt_required()
def unregister_activity(activity_id):
    """取消报名"""
    try:
        user_id = get_jwt_identity()
        
        registration = Registration.query.filter_by(
            user_id=user_id, activity_id=activity_id
        ).first()
        
        if not registration:
            return jsonify({'error': 'Registration not found'}), 404
        
        if registration.status not in ['registered']:
            return jsonify({'error': 'Cannot cancel registration at this stage'}), 400
        
        # 取消报名
        registration.cancel()
        
        # 更新活动参与人数
        activity = Activity.query.get(activity_id)
        if activity:
            activity.current_participants = max(0, activity.current_participants - 1)
        
        db.session.commit()
        
        return jsonify({'message': 'Registration cancelled successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500