from app import db
from datetime import datetime

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    max_participants = db.Column(db.Integer, default=50)
    current_participants = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    category = db.Column(db.String(50))  # 环保、助老、教育等
    volunteer_hours = db.Column(db.Float, default=0.0)  # 可获得的志愿时长
    requirements = db.Column(db.Text)  # 报名要求
    contact_person = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    image_url = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    registrations = db.relationship('Registration', backref='activity', lazy=True)
    creator = db.relationship('User', backref='created_activities')
    
    @property
    def is_full(self):
        """检查活动是否已满员"""
        return self.current_participants >= self.max_participants
    
    @property
    def is_active(self):
        """检查活动是否仍在进行中"""
        return self.status == 'active' and self.start_time > datetime.utcnow()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'max_participants': self.max_participants,
            'current_participants': self.current_participants,
            'status': self.status,
            'category': self.category,
            'volunteer_hours': self.volunteer_hours,
            'requirements': self.requirements,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'image_url': self.image_url,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_full': self.is_full,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Activity {self.title}>'