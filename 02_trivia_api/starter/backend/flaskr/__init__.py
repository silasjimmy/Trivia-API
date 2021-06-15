import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

# Helper functions

def paginate_questions(request, selection):
    '''
    Paginates the questions to 10 questions per page.

    Parameters:
        request (obj): Request object
        selection (list): List of questions

    Returns:
        current_questions (list): List of paginated questions
    '''

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]

    return current_questions

def random_question(questions):
    '''
    Selects a random question from questions

    Parameters:
        questions (list): List of question objects

    Returns:
        question (obj): A single question objetc
    '''

    selected_question = questions[random.randrange(0, len(questions), 1)]
    return selected_question

def question_used(question, previous_questions):
    '''
    Checks if the question is among the previous questions.

    Parameters:
        question (obj): Question object.
        previous_questions (list): List of previous questions.

    Returns:
        bool: True if the question is a previous question, False otherwise.
    '''

    if question.id in previous_questions:
        return True

# Create app function

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    # DONE
    cors = CORS(app, resources={r"/api/*": {'origins': "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    # DONE
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    # DONE
    @app.route('/categories')
    def get_categories():
        '''
        Handles GET requests for all available categories
        '''

        categories = Category.query.all()

        categories_dict = {
            category.id:category.type for category in categories
        }

        # Check if the dictionary actually contains anything
        if categories_dict:
            return jsonify({
                'success': True,
                'categories': categories_dict
            })
        else:
            abort(404)


    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    # DONE
    @app.route('/questions')
    def get_questions():
        '''
        Handles GET requests for questions with pagination
        '''

        # Get the paginated questions
        questions = Question.query.all()
        paginated_questions = paginate_questions(request, questions)

        # Get all categories and create a dictionary
        categories = Category.query.all()
        categories_dict = {
            category.id:category.type for category in categories
        }

        # Check if there are any questions
        if paginated_questions:
            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(questions),
                # 'current_category': 'Category',
                'categories': categories_dict
            })
        else:
            abort(404)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    # DONE
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''
        Handles DELETE requests for specific questions using the question id
        '''

        try:
            question = Question.query.filter(Question.id==question_id).one_or_none()
            question.delete()

            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    # DONE
    @app.route('/questions', methods=['POST'])
    def add_question():
        '''
        Handles POST requests for creating and posting new questions
        '''

        data = request.get_json()

        try:
            new_question = Question(
                question=data.get('question', None),
                answer=data.get('answer', None),
                category=data.get('category', None),
                difficulty=data.get('difficulty', None)
            )

            new_question.insert()

            return jsonify({
                'success': True
            })
        except Exception:
            abort(422)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/search/questions', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('searchTerm', None)

        if search_term:
            try:
                questions_query = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
                paginated_questions = paginate_questions(request, questions_query)

                return jsonify({
                    'success': True,
                    'questions': paginated_questions,
                    'total_questions': len(paginated_questions)
                })
            except Exception:
                abort(422)
        else:
            abort(404)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    # DONE
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        '''
        Handles GET requests of questions based on a specific category
        '''

        category = Category.query.filter(Category.id==category_id).one_or_none()

        if category == None:
            abort(404)

        try:
            questions_query = Question.query.filter(Question.category==category.id).all()
            paginated_questions = paginate_questions(request, questions_query)

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(paginated_questions),
                'current_category': category.type
            })
        except Exception:
            abort(422)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_question():
        data = request.get_json()

        previous_questions = data.get('previous_questions', None)
        category = data.get('quiz_category', None)

        # Not found if there are no previous questions or category provided
        if previous_questions == None or category == None:
            abort(404)

        try:
            # Get questions based on the provided category
            if category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category==category['id']).all()

            # Get the unused questions
            unused_questions = [question for question in questions \
                if not question_used(question, previous_questions)]

            # Selecte a random question to play
            selected_question = random_question(unused_questions)

            return jsonify({
                'success': True,
                'question': selected_question.format()
            })
        except Exception:
            abort(422)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not found error"
        }), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': "Forbidden error"
        }), 403

    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable entity error"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal server error"
        }), 500

    return app
