from models import db, RecyclingRecord, User, RecyclingItem
from datetime import datetime, timedelta
from sqlalchemy import func, desc


class RecyclingAnalytics:
    @staticmethod
    def get_user_stats(user_id):
        """Get comprehensive statistics for a user"""
        total_points = db.session.query(func.sum(RecyclingRecord.points_earned)) \
                           .filter(RecyclingRecord.user_id == user_id).scalar() or 0

        total_items = RecyclingRecord.query.filter_by(user_id=user_id).count()

        # Most recycled item
        most_recycled = db.session.query(
            RecyclingRecord.item_name,
            func.count(RecyclingRecord.id).label('count')
        ).filter(RecyclingRecord.user_id == user_id) \
            .group_by(RecyclingRecord.item_name) \
            .order_by(desc('count')).first()

        # Weekly activity
        week_ago = datetime.utcnow() - timedelta(days=7)
        weekly_items = RecyclingRecord.query.filter(
            RecyclingRecord.user_id == user_id,
            RecyclingRecord.recycled_at >= week_ago
        ).count()

        return {
            'total_points': total_points,
            'total_items': total_items,
            'most_recycled_item': most_recycled[0] if most_recycled else None,
            'most_recycled_count': most_recycled[1] if most_recycled else 0,
            'weekly_activity': weekly_items
        }

    @staticmethod
    def get_community_stats():
        """Get community-wide statistics"""
        total_users = User.query.count()
        total_recycled_items = RecyclingRecord.query.count()
        total_points_earned = db.session.query(func.sum(RecyclingRecord.points_earned)).scalar() or 0

        # Top recyclers
        top_recyclers = db.session.query(
            User.username,
            func.sum(RecyclingRecord.points_earned).label('total_points')
        ).join(RecyclingRecord) \
            .group_by(User.id) \
            .order_by(desc('total_points')) \
            .limit(5).all()

        # Most popular items
        popular_items = db.session.query(
            RecyclingRecord.item_name,
            func.count(RecyclingRecord.id).label('recycle_count')
        ).group_by(RecyclingRecord.item_name) \
            .order_by(desc('recycle_count')) \
            .limit(5).all()

        return {
            'total_users': total_users,
            'total_recycled_items': total_recycled_items,
            'total_points_earned': total_points_earned,
            'top_recyclers': [{'username': u[0], 'points': u[1]} for u in top_recyclers],
            'popular_items': [{'item': i[0], 'count': i[1]} for i in popular_items]
        }

    @staticmethod
    def get_category_distribution(user_id=None):
        """Get recycling distribution by category"""
        query = db.session.query(
            RecyclingItem.category,
            func.count(RecyclingRecord.id).label('count')
        ).join(RecyclingRecord, RecyclingRecord.item_name == RecyclingItem.name)

        if user_id:
            query = query.filter(RecyclingRecord.user_id == user_id)

        distribution = query.group_by(RecyclingItem.category).all()

        return {cat: count for cat, count in distribution}