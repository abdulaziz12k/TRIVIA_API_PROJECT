# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.


##  Getting started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 


#### Error handling 
- Errors excpected 
- 404: Not found
- 422: Unprocessable Entity
- 500: Internal Server Error
- Errors are formated using Json with this format:
({"success": False,
 "error": 404,
 "message": "resource not found"
 })
### Endpoints 

#### GET /categories
- General:
    - Returns a list of all categories with a success result
- Sample: `curl http://127.0.0.1:5000/categories`

{"categories":
[{"id":1,"type":"Science"},
{"id":2,"type":"Art"},
{"id":3,"type":"Geography"},
{"id":4,"type":"History"},
{"id":5,"type":"Entertainment"},
{"id":6,"type":"Sports"}],
"success":true}

#### GET /questions
- General:
    - Returns a list of all questions paginated 10 at each page, and total number of questions
- Sample: `curl http://127.0.0.1:5000/questions`

{"categories":[
    {"id":1,"type":"Science"},
    {"id":2,"type":"Art"},
    {"id":3,"type":"Geography"},
    {"id":4,"type":"History"},
    {"id":5,"type":"Entertainment"},
    {"id":6,"type":"Sports"}],
"currentCategory":null,"questions":[
    {"answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},
    {"answer":"Tom Cruise","category":5,"difficulty":4,"id":4,"question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},
    {"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
    {"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
    {"answer":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"},
    {"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"},
    {"answer":"Uruguay","category":6,"difficulty":4,"id":11,"question":"Which country won the first ever soccer World Cup in 1930?"},{"answer":"George Washington Carver","category":4,"difficulty":2,"id":12,"question":"Who invented Peanut Butter?"},{"answer":"Lake Victoria","category":3,"difficulty":2,"id":13,"question":"What is the largest lake in Africa?"},{"answer":"The Palace of Versailles","category":3,"difficulty":3,"id":14,"question":"In which royal palace would you find the Hall of Mirrors?"}],
    "totalQuestions":19}

#### DELETE /questions/{question_id}/delete
- General:
    - Deletes a question based on an id if it is exists then shows the list of questions
    - Results are returned in jsonify format Including the success of the operation, question deleted, and the list of questions.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/23/delete`

{"deleted_book":{"answer":"One","category":2,"difficulty":4,"id":18,"question":"How many paintings did Van Gogh sell in his lifetime?"},"questions":[{"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
{"answer":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"},
{"answer":"Apollo 13","category":5,"difficulty":4,"id":2,"question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"},{"answer":"Tom Cruise","category":5,"difficulty":4,"id":4,"question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},
{"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
{"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"},{"answer":"Uruguay","category":6,"difficulty":4,"id":11,"question":"Which country won the first ever soccer World Cup in 1930?"},
{"answer":"George Washington Carver","category":4,"difficulty":2,"id":12,"question":"Who invented Peanut Butter?"},
{"answer":"Lake Victoria","category":3,"difficulty":2,"id":13,"question":"What is the largest lake in Africa?"},
{"answer":"Agra","category":3,"difficulty":2,"id":15,"question":"The Taj Mahal is located in which Indian city?"},
{"answer":"Escher","category":2,"difficulty":1,"id":16,"question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"},{"answer":"Mona Lisa","category":2,"difficulty":3,"id":17,"question":"La Giaconda is better known as what?"},
{"answer":"One","category":2,"difficulty":4,"id":18,"question":"How many paintings did Van Gogh sell in his lifetime?"}],
"success":true}

#### POST /questions/submit 
- GENERAL:
    - submit a new question to the database by sending a POST request with the question data as JSON, and returns a JSON response indicating whether the operation was successful or not
    - Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"question\": \"where is karem benzema new contract?\", \"answer\": \"saudi arabia\", \"difficulty\": 3, \"category\": \"6\"}" http://127.0.0.1:5000/questions/submit`

{"question":true}

#### POST /questions/search 
- GENERAL:
    - searches for questions based on a search term then returns a Json formated response similiar to the search term
    - Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"searchTerm\": \"benzema\"}" http://localhost:5000/questions/search`

[{"question":
"where is karem benzema new contract?"
}]

#### GET /category/{category_id}/questions
- GENERAL:
    - searches for questions by it's category based on a request parameter of {category_id} 
    - Sample: `curl http://127.0.0.1:5000/categories/6/questions?category=6`

{"current_category":
:"6",
"questions":
[{"category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"},
{"category":6,"difficulty":4,"id":11,"question":"Which country won the first ever soccer World Cup in 1930?"},
{"category":6,"difficulty":3,"id":24,"question":"where is karem benzema new contract?"}],
"total_questions":3}

#### POST /quizzes
- GENERAL:
    - quiz game allow user to play with random question that is not within th previous questions.
    - Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"previous_questions\": [16, 17], \"quiz_category\": 3}" http://http://127.0.0.1:5000/quizzes`

{"question":
{"answer":"Agra",
"category":3,
"difficulty":2,
"id":15,
"question":
"The Taj Mahal is located in which Indian city?"},
"succes":true}




### AUTHORS
Udacity

### CONTRIBUTES
 Abdulaziz I. Hijazi