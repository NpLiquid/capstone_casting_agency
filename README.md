# The ultimate trivia test

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

Please navigate to the backend folder to consult a more comprehensive README file.

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

Please navigate to the frontend folder to consult a more comprehensive README file.

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting started

- Base URL: At present this app can only be run locally and it is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration

- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Erros are returned as JSON objects in the following format

```javascript
{
 'success': False,
 'error': 400,
 'message': "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource not Found
- 422: Not Processable

### Endpoints

#### GET/categories

- General:
    - Returns a list of category objects and success value.
- Sample: ``` curl http://127.0.0.1:5000/categories ```

```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### GET/categories/{category_id}/questions

- General:
    - Returns a list of questions objects belonging to a category ID, success value, total number of questions belonging to a category ID, and the type of the category.
- Sample: ``` curl http://127.0.0.1:5000/categories/2/questions ```

```javascript
{
  "current_category": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

#### GET/questions

- General:
    - Returns a list of question objects, a list of category objects, success value, and total number of questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: ``` curl http://127.0.0.1:5000/questions ```

```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```

#### POST/questions

- General:
    - Creates a new question using the submitted question, answer, difficulty, and category. Returns the id of the created question, success value, created question, category of the created question, total number of questions, and question list based on current page number to update the frontend.
- Sample: ``` curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"In which continent is located Mexico?","answer":"America","difficulty":"1","category":"3"}' ```

```javascript

{
  "created": 38, 
  "current_category": 3, 
  "question_created": "In which continent is located Mexico?", 
  "questions": [
    {
      "answer": "America", 
      "category": 3, 
      "difficulty": 1, 
      "id": 38, 
      "question": "In which continent is located Mexico?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}

```

#### POST/questions/search

- General:
    - Returns a list of question objects based on a search term, success value, and total number of questions on current page number to update the frontend.
- Sample: ``` curl http://127.0.0.1:5000/questions/search?page=1 -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Africa"}' ```


```javascript

{
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

```

#### POST/quizzes

- General:
    - Allows the user to play quizzes in the frontend.
    - Returns a random question object based on a category and a success value.
- Sample: ``` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Art", "id": "2"}}' ```

```javascript

{
  "question": {
    "answer": "Jackson Pollock", 
    "category": 2, 
    "difficulty": 2, 
    "id": 19, 
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  }, 
  "success": true
}

```

#### DELETE/questions/{question_id}

- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value
- Sample: ``` curl -X DELETE http://127.0.0.1:5000/questions/36  ```

```javascript
{
  "deleted": 36, 
  "success": true
}
```

## Authors

The base code is part of the Udacity Full Stack Web Developer Course.

Modifications to backend and test files were done by Ari Yair Barrera Animas.
