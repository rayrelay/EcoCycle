# [file name]: ecocycle_app.py
from flask import Flask, render_template, request, jsonify, session, url_for, redirect
import random
from datetime import datetime
from models import db, RecyclingItem, User, RecyclingRecord, Category
from database_init import DatabaseInitializer
from analytics import RecyclingAnalytics
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ecocycle.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Default user ID for demo (in real app, use proper authentication)
DEFAULT_USER_ID = 1


def initialize_database():
    """Initialize database tables and data"""
    with app.app_context():
        db.create_all()
        DatabaseInitializer.init_data()

        # Create default user if not exists
        if not User.query.get(DEFAULT_USER_ID):
            default_user = User(id=DEFAULT_USER_ID, username='demo_user')
            db.session.add(default_user)
            db.session.commit()
        print("Database initialized successfully!")


# Initialize database when app starts
initialize_database()


def get_current_user():
    """Get current user (simplified for demo)"""
    return User.query.get(DEFAULT_USER_ID)


@app.route('/')
def index():
    user = get_current_user()
    categories = Category.query.all()
    return render_template('ecocycle_index.html', user_data=user.to_dict(), categories=categories)


@app.route('/recycle', methods=['POST'])
def recycle():
    item_name = request.form['item'].lower()
    user = get_current_user()

    recycling_item = RecyclingItem.query.filter_by(name=item_name).first()

    if recycling_item:
        # Create recycling record
        record = RecyclingRecord(
            user_id=user.id,
            item_name=item_name,
            points_earned=recycling_item.points
        )

        # Update user points and level
        user.points += recycling_item.points

        # Check for level up
        if user.points >= user.next_reward:
            user.level += 1
            user.next_reward = user.level * 50

        db.session.add(record)
        db.session.commit()

        # Convert tips from JSON string to list
        import json
        tips = json.loads(recycling_item.tips) if recycling_item.tips else []

        return render_template('ecocycle_results.html',
                               item=item_name,
                               instruction=recycling_item.instruction,
                               points=recycling_item.points,
                               category=recycling_item.category,
                               tips=tips,
                               user_data=user.to_dict())
    else:
        return render_template('ecocycle_results.html',
                               item=item_name,
                               instruction="We're not sure how to recycle this item. Please check with your local recycling facility.",
                               points=0,
                               category="Unknown",
                               tips=["Try searching for similar items", "Contact your local waste management"],
                               user_data=user.to_dict())


@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    results = []

    if query:
        items = RecyclingItem.query.filter(RecyclingItem.name.contains(query)).all()
        results = [{"item": item.name, "category": item.category} for item in items]

    return jsonify(results)


# New API endpoints for data collection and reporting
@app.route('/api/user/stats')
def api_user_stats():
    """API endpoint for user statistics"""
    user = get_current_user()
    stats = RecyclingAnalytics.get_user_stats(user.id)
    return jsonify(stats)


@app.route('/api/community/stats')
def api_community_stats():
    """API endpoint for community statistics"""
    stats = RecyclingAnalytics.get_community_stats()
    return jsonify(stats)


@app.route('/api/recycling/records')
def api_recycling_records():
    """API endpoint for recycling records with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    user = get_current_user()
    records = RecyclingRecord.query.filter_by(user_id=user.id) \
        .order_by(RecyclingRecord.recycled_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    records_data = [{
        'item_name': record.item_name,
        'points_earned': record.points_earned,
        'recycled_at': record.recycled_at.isoformat()
    } for record in records.items]

    return jsonify({
        'records': records_data,
        'total': records.total,
        'pages': records.pages,
        'current_page': page
    })


@app.route('/report')
def report():
    """Reporting dashboard"""
    user = get_current_user()
    user_stats = RecyclingAnalytics.get_user_stats(user.id)
    community_stats = RecyclingAnalytics.get_community_stats()
    category_dist = RecyclingAnalytics.get_category_distribution(user.id)

    # 获取用户最近回收记录
    recent_records = RecyclingRecord.query.filter_by(user_id=user.id) \
        .order_by(RecyclingRecord.recycled_at.desc()) \
        .limit(5).all()

    return render_template('ecocycle_report.html',
                           user_data=user.to_dict(),
                           user_stats=user_stats,
                           community_stats=community_stats,
                           category_dist=category_dist,
                           recent_records=recent_records)


if __name__ == '__main__':
    app.run(debug=True)