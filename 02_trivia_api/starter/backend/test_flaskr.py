import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'sliman17', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        '''
        Tests the GET request for categories
        '''

        response = self.client().get('/categories')
        response_data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['categories'])

    def test_get_questions(self):
        '''
        Tests the GET request for paginated questions
        '''

        response = self.client().get('/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['categories'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['questions'])

    def test_delete_question(self):
        '''
        Tests the DELETE request to delete a question
        '''

        response = self.client().delete('/questions/5')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_add_question(self):
        '''
        Tests the POST request to add a new question
        '''

        data = {
            'question': 'Who is the strongest man alive',
            'answer': 'no one',
            'difficulty': 5,
            'category': 3,
        }

        response = self.client().post('/questions', json=data)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_search_questions(self):
        '''
        Tests the POST request to search for a question
        '''

        request_data = {
            'searchTerm': '1930',
        }

        response = self.client().post('/search/questions', json=request_data)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])

    def test_get_category_questions(self):
        '''
        Tests the GET request for getting questions by category
        '''
        
        response = self.client().get('/categories/1/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['current_category'])

    def test_play_question(self):
        '''
        Tests the POST request for playing questions
        '''

        request_data = {
            'previous_questions': [5, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
            }
        }

        response = self.client().post('/quizzes', json=request_data)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
