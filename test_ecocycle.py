import unittest
from ecocycle_app import app, db
from models import User, RecyclingItem, RecyclingRecord
from database_init import DatabaseInitializer
from unittest.mock import patch
import json


class EcoCycleTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()
            DatabaseInitializer.init_data()

    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EcoCycle', response.data)

    def test_search_api(self):
        """Test search API endpoint"""
        response = self.app.get('/api/search?q=plastic')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)

    def test_recycle_item(self):
        """Test recycling an item"""
        with app.app_context():
            user = User.query.get(1)
            initial_points = user.points

            response = self.app.post('/recycle', data={'item': 'plastic bottle'})
            self.assertEqual(response.status_code, 200)

            # Check points increased
            user = User.query.get(1)
            self.assertGreater(user.points, initial_points)

    @patch('ecocycle_app.RecyclingAnalytics.get_user_stats')
    def test_user_stats_api(self, mock_stats):
        """Test user stats API with mock"""
        mock_stats.return_value = {'total_points': 100, 'total_items': 10}

        response = self.app.get('/api/user/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total_points'], 100)

    def test_recycling_record_creation(self):
        """Test recycling record is created properly"""
        with app.app_context():
            response = self.app.post('/recycle', data={'item': 'paper'})
            record = RecyclingRecord.query.first()

            self.assertIsNotNone(record)
            self.assertEqual(record.item_name, 'paper')


if __name__ == '__main__':
    unittest.main()