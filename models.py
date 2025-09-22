from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class RecyclingItem(db.Model):
    __tablename__ = 'recycling_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tips = db.Column(db.Text)  # Store as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json
        return {
            'name': self.name,
            'instruction': self.instruction,
            'points': self.points,
            'category': self.category,
            'tips': json.loads(self.tips) if self.tips else []
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    next_reward = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'points': self.points,
            'level': self.level,
            'next_reward': self.next_reward
        }


class RecyclingRecord(db.Model):
    __tablename__ = 'recycling_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    points_earned = db.Column(db.Integer, nullable=False)
    recycled_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('records', lazy=True))


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), default='#2e8b57')  # Hex color
    description = db.Column(db.Text)