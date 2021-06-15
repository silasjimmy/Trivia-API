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
        Test for getting all categories
        '''

        response = self.client().get('/categories')
        response_data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['categories'])

    def test_get_questions(self):
        '''
        Test for getting paginated questions
        '''

        response = self.client().get('/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['categories'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['questions'])

    def test_page_out_of_bound(self):
        """
        Test for out of bound page
        """

        response = self.client().get('/questions?page=100')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found error')

    def test_delete_question(self):
        '''
        Test to delete a question
        '''

        response = self.client().delete('/questions/5')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_delete_question_with_id_not_exist(self):
        """
        Test deletion of question whose id doesn't exist
        """

        response = self.client().delete('/questions/100')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Unprocessable entity error')

    def test_add_question(self):
        '''
        Test to add a new question
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

    def test_add_question_with_empty_data(self):
        """
        Test for a case where fields have empty data
        """

        request_data = {
            'question': '',
            'answer': '',
            'difficulty': 3,
            'category': 3,
        }

        response = self.client().post('/questions', json=request_data)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Unprocessable entity error')

    def test_search_questions(self):
        '''
        Test for searching for a question
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

    def test_search_term_is_empty(self):
        """
        Test for empty string as a search term
        """

        request_data = {
            'searchTerm': '',
        }

        response = self.client().post('/search/questions', json=request_data)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found error')

    def test_get_category_questions(self):
        '''
        Test for getting questions by category
        '''

        response = self.client().get('/categories/1/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['questions'])
        self.assertTrue(response_data['total_questions'])
        self.assertTrue(response_data['current_category'])

    def test_invalid_category_id(self):
        """
        Test for invalid category id
        """

        response = self.client().get('/categories/100/questions')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found error')

    def test_play_question(self):
        '''
        Test for playing questions
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

    def test_no_more_questions_to_play(self):
        """
        Test for the case where no more questions to play
        """

        response = self.client().post('/quizzes', json={})
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found error')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
