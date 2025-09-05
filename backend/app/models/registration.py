from app import db
from datetime import datetime

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    status = db.Column(db.String(20), default='registered')  # registered, checked_in, completed, cancelled
    registration_time = db.Column(db.DateTime, default=datetime.utcnow)
    check_in_time = db.Column(db.DateTime)
    completion_time = db.Column(db.DateTime)
    notes = db.Column(db.Text)  # 备注信息
    rating = db.Column(db.Integer)  # 活动评分 1-5
    feedback = db.Column(db.Text)  # 反馈意见
    
    # 复合唯一约束，确保用户不能重复报名同一活动
    __table_args__ = (db.UniqueConstraint('user_id', 'activity_id', name='unique_user_activity'),)
    
    def check_in(self):
        """签到"""
        if self.status == 'registered':
            self.status = 'checked_in'
            self.check_in_time = datetime.utcnow()
            return True
        return False
    
    def complete(self, rating=None, feedback=None):
        """完成活动"""
        if self.status == 'checked_in':
            self.status = 'completed'
            self.completion_time = datetime.utcnow()
            if rating:
                self.rating = rating
            if feedback:
                self.feedback = feedback
            return True
        return False
    
    def cancel(self):
        """取消报名"""
        if self.status in ['registered', 'checked_in']:
            self.status = 'cancelled'
            return True
        return False
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_id': self.activity_id,
            'status': self.status,
            'registration_time': self.registration_time.isoformat() if self.registration_time else None,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'completion_time': self.completion_time.isoformat() if self.completion_time else None,
            'notes': self.notes,
            'rating': self.rating,
            'feedback': self.feedback
        }
    
    def __repr__(self):
        return f'<Registration User:{self.user_id} Activity:{self.activity_id}>'