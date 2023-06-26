import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from config import *
from models import *
from flaskr import *



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        # binds the app to the current context


    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    #GET CATEGORIES
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"], True)
        self.assertEqual(data["success"], True)   
    
    #if the database has no categories_ deleting all categories accordingly
    def test_404_get_categories_failure(self):
        Category.query.delete()
        db.session.commit()

        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    #-----------------------------------------------------------------------------
    
    #QUESTIONS PAGE TESTS
    def test_questions_page(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"], True)
        self.assertTrue(data["totalQuestions"] > 0)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    #--------------------------------------------------------------------------
    
    #QUESTION DELETION
    def test_delete_question(self):
        res = self.client().delete('/questions/10/delete')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_404_question_does_not_exist(self):
        res = self.client().delete('/questions/1000000/delete')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")
        print(f"{data}")
    #-------------------------------------------------------------------------

    #SUBMITING QUESTION
    def test_submit_question(self):
        new_question = {
            "question": "if you had one chance will you take it or let it slip?",
            "answer": "Take it",
            "difficulty": 1,
            "category": 1,
            }
        res = self.client().post('/questions/submit', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["question"], True)

    def test_422_submit_question_failed(self):
        new_question = {
        "question": "a",
        "answer": "a",
        "difficulty": 1,
        "category": 10,
        }
        res = self.client().post('/questions/submit', json=new_question)
        self.assertEqual(res.status_code, 422)
    #--------------------------------------------------------------------------
    
    # #GETTING QUESTION BY CATEGORY
    def test_get_question_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], None)

    def test_404_get_question_by_invalid_category(self):
        res = self.client().get('/categories/1000000/questions')
        self.assertEqual(res.status_code, 404)
        
    #--------------------------------------------------------------------------
    
    # #SEARCTHING FOR QUESTION
    def test_search_question_success(self):
        res = self.client().post("/questions/search", json={"searchTerm": "movie"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data) > 0)
        
    def test_404_search_question_failed(self):
        res = self.client().post("/questions/search", json={"searchTerm": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    #------------------------------------------------------------------
        
    # #QUIZES FROM QUESTIONS 
    def test_get_quiz_questions(self):
        quiz_data = {
            "previous_questions": [],
            "quiz_category": 2
        }
        res = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])

    def test_500_get_quiz_questions_failed(self):
        quiz_data = {
        "previous_questions": [0],
        "quiz_category": 0
        }
        res = self.client().post('/quizzes', json=quiz_data)
        self.assertEqual(res.status_code, 500)

    #--------------------------------------------------------------------------
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()