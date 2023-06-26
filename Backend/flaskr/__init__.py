import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_cors import CORS
import random
from random import choice
from models import *
from traceback import print_exc
import sys
from math import ceil
from config import *


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    question = [question.format() for question in selection]
    sorted_questions = question[start:end]
    return sorted_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authentication,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    # GET CATEGORIES
    @app.route("/categories", methods=["GET"])
    def show_categories():
        response = Category.query.order_by(Category.id).all()
        try:
            # if response is None:
            #     abort(404)
            # else:
                categories = [category.format() for category in response]
                return jsonify({
                    "categories": categories,
                    "success": True
                })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    # GET QUESTIONS
    @app.route("/questions")
    def questions_page():
        selection = Question.query.order_by(Question.id).all()
        sort_questions = paginate_questions(request, selection)
        page = request.args.get("page", 1, type=int)
        per_page = 10
        total_pages = ceil(len(selection) / per_page)
        if page > total_pages:
            abort(404)
        else:
            current_category = request.args.get("category", None, type=int)

            return jsonify({
                        "questions": sort_questions,
                        "totalQuestions": len(selection),
                        "currentCategory": current_category,
                        "categories": [
                            category.format()
                            for category in Category.query.order_by(Category.id).all()
                        ]})

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    # DELETING QUESTION
    @app.route("/questions/<int:question_id>/delete", methods=["DELETE"])
    def delete_question(question_id):
        # print(f"Deleting question with ID: {question_id}")
        question = Question.query.filter_by(id=question_id).first()
        paginated_questions = [question.format() for question in Question.query.all()]
        if question is None:
            # print(f"Question with ID {question_id} not found")
            abort(404)
        else:
            deleted_question = question.format()
            question.delete()
            return jsonify({
                "success": True,
                    "deleted_book": deleted_question,
                    "questions": paginated_questions,
                })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    # SUMBITING QUESTIONS
    @app.route("/questions/submit", methods=["POST"])
    def submit_question():
        response = request.get_json()
        try:
            if response is None:
                abort(404)
            else:
                new_question = Question(
                    question=response.get("question"),
                    answer=response.get("answer"),
                    difficulty=response.get("difficulty"),
                    category=response.get("category"),
                )
                new_question.insert()
                return jsonify({"question": True})
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    # SERACH FOR QUESTION
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        data = request.get_json()
        if data is None or data["searchTerm"].strip() == "":
            abort(404)
        else:
            searchTerm = data["searchTerm"]
            search_results = Question.query.filter(
                or_(Question.question.ilike("%{}%".format(searchTerm)))
            )
            results = [
                {"question": question.question} for question in search_results.all()
            ]
        return jsonify(results)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    # SEARCH FOR QUESTION BY CATEGORY
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        response = Category.query.get(category_id)
        if response is None:
            abort(404) 
        else:
            questions = Question.query.filter_by(category=category_id).all()
            formatted_questions = [i.format() for i in questions]
            for question in formatted_questions:
                question.pop("answer", None)
            current_category = request.args.get("category", None)
            return jsonify(
                    {
                    "questions": formatted_questions,
                    "total_questions": len(formatted_questions),
                    "current_category": current_category,
                    }
                )

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    # QUIZES FROM QUESTIONS
    @app.route("/quizzes", methods=["POST"])
    def get_quiz_questions():
        data = request.get_json()
        try:
            if data is None:
                abort(404)
            else:
                previous_questions = data.get("previous_questions")
                quiz_category = data.get("quiz_category")
                print(quiz_category)
                questions = (
                    Question.query.filter_by(category=quiz_category['id'])
                    .filter(Question.id.notin_(previous_questions))
                    .all()
                )
                question = choice(questions) if questions else None
                return jsonify(
                    {
                        "success": True,
                        "question": question.format() if question else None,
                    }
                )
        except Exception as e:
            return (
                jsonify(
                    {
                        "error": str(e),
                        "message": "An error occurred while processing your request",
                    }
                ),
                500,
            )

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({"message": "An error occurred while processing your request"})

    return app


app = create_app()
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
