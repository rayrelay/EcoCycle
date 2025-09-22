# [file name]: database_init.py
import json
from models import db, RecyclingItem, Category


class DatabaseInitializer:
    @staticmethod
    def init_data():
        """Initialize the database with default data"""
        DatabaseInitializer.init_categories()
        DatabaseInitializer.init_recycling_items()

    @staticmethod
    def init_categories():
        """Initialize categories"""
        categories = [
            {'name': 'Plastic', 'color': '#4a90e2', 'description': 'Plastic materials'},
            {'name': 'Paper', 'color': '#f39c12', 'description': 'Paper and cardboard'},
            {'name': 'Glass', 'color': '#2e8b57', 'description': 'Glass containers'},
            {'name': 'Metal', 'color': '#95a5a6', 'description': 'Metal cans and items'},
            {'name': 'E-Waste', 'color': '#e74c3c', 'description': 'Electronic waste'},
            {'name': 'Hazardous', 'color': '#c0392b', 'description': 'Hazardous materials'},
            {'name': 'Organic', 'color': '#8e44ad', 'description': 'Organic waste'}
        ]

        for cat_data in categories:
            if not Category.query.filter_by(name=cat_data['name']).first():
                category = Category(**cat_data)
                db.session.add(category)

        db.session.commit()

    @staticmethod
    def init_recycling_items():
        """Initialize recycling items"""
        items_data = [
            {
                "name": "plastic bottle",
                "instruction": "Rinse and remove caps. Place in blue recycling bin.",
                "points": 5,
                "category": "Plastic",
                "tips": ["Crush bottles to save space", "Remove labels if possible"]
            },
            {
                "name": "paper",
                "instruction": "Keep dry and clean. Place in blue recycling bin.",
                "points": 3,
                "category": "Paper",
                "tips": ["Flatten cardboard boxes", "Remove any plastic wrapping"]
            },
            {
                "name": "cardboard",
                "instruction": "Flatten boxes. Place in blue recycling bin.",
                "points": 4,
                "category": "Paper",
                "tips": ["Break down large boxes", "Remove packing tape"]
            },
            {
                "name": "glass bottle",
                "instruction": "Rinse thoroughly. Place in green glass recycling bin.",
                "points": 6,
                "category": "Glass",
                "tips": ["Remove metal caps", "Don't break glass - it's harder to recycle"]
            },
            {
                "name": "aluminum can",
                "instruction": "Rinse and crush if possible. Place in blue recycling bin.",
                "points": 8,
                "category": "Metal",
                "tips": ["Crushing saves space", "Check for local redemption value"]
            },
            {
                "name": "electronics",
                "instruction": "Take to designated e-waste recycling center. Do not place in regular bins.",
                "points": 15,
                "category": "E-Waste",
                "tips": ["Remove batteries if possible", "Wipe personal data from devices"]
            },
            {
                "name": "battery",
                "instruction": "Take to special battery recycling drop-off location. Hazardous if disposed improperly.",
                "points": 10,
                "category": "Hazardous",
                "tips": ["Tape terminals of lithium batteries", "Store in cool, dry place until recycling"]
            },
            {
                "name": "plastic bag",
                "instruction": "Take to grocery store recycling bin. Do not place in curbside recycling.",
                "points": 2,
                "category": "Plastic",
                "tips": ["Reuse when possible", "Collect multiple bags together for recycling"]
            },
            {
                "name": "food waste",
                "instruction": "Compost if possible. Otherwise dispose in regular trash.",
                "points": 0,
                "category": "Organic",
                "tips": ["Start a compost bin", "Use a countertop compost collector"]
            }
        ]

        for item_data in items_data:
            if not RecyclingItem.query.filter_by(name=item_data['name']).first():
                # Convert tips list to JSON string
                tips_json = json.dumps(item_data.pop('tips'))
                item = RecyclingItem(**item_data)
                item.tips = tips_json
                db.session.add(item)

        db.session.commit()