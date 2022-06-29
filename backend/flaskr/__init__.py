import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # GET requests for all available categories.
    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        return jsonify({"success": True,
                        "categories": {
                            category.id: category.type for category in categories
                        }})

    # GET requests for questions, including pagination (every 10 questions).
    @app.route("/questions")
    def get_questions():
        categories = Category.query.order_by(Category.id).all()
        questions = Question.query.order_by(Question.id).all()

        quest_results = paginate_questions(request, questions)

        return jsonify({"success": True,
                        "questions": quest_results,
                        "total_questions": len(questions),
                        "categories": {
                            category.id: category.type for category in categories
                        }})

    # DELETE question using a question ID.
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.all()
            current_questions = paginate_questions(request, questions)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(questions),
                }
            )

        except:
            abort(422)

    """
    Creating an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=['POST'])
    def create_questions():
        body = request.get_json()

        added_question = body.get("question", None)
        added_answer = body.get("answer", None)
        added_category = body.get("category", None)
        added_difficulty = body.get("difficulty", None)

        try:
            if added_question is None:
                abort(400)

            if added_answer is None:
                abort(400)

            if added_difficulty is None:
                abort(400)

            if added_category is None:
                abort(400)
            else:
                question = Question(
                    question=added_question,
                    answer=added_answer,
                    category=added_category,
                    difficulty=added_difficulty)

                question.insert()
                questions = Question.query.all()

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "total_questions": len(questions)
                    }
                )

        except:
            abort(422)

    """
    Creating POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get("searchTerm", None)

        try:
            questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search))).all()
            current_questions = paginate_questions(request, questions)

            if len(current_questions) == 0:
                return jsonify({
                    'success': False,
                    'total_questions': len(current_questions)
                })
            else:
                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(current_questions)
                })

        except:
            abort(422)

    """
    Creating a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def question_by_category(category_id):
        categories = Category.query.order_by(Category.id).all()
        category = Category.query.get(category_id)

        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            current_questions = paginate_questions(request, questions)
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(current_questions),
                "categories": {
                    category.id: category.type for category in categories
                },
                "category_now": category.id
            })
        except:
            abort(422)

    """
    Creating a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def random_questions():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body['quiz_category']['id']

        try:
            if quiz_category:
                questions = Question.query.filter(
                    Question.category == quiz_category).all()
            else:
                questions = Question.query.all()

            current_questions = [question.format() for question in questions]
            random_question = random.choice(current_questions)

            while random_question['id'] in previous_questions:
                if len(previous_questions) == len(current_questions):
                    random_question = None
                    break

                random_question = random.choice(current_questions)

            return jsonify({
                "success": True,
                "question": random_question
            })
        except:
            abort(422)

    # Creating error handlers for all expected errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'status': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
