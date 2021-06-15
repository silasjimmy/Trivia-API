# Trivia API

Trivia API is an Application Programming Interface made for the Udacitrivia web app, a platform made to hold trivial subjects and play word games.

## Getting started

### Installing dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Enviornment** - Since the API can only be used locally for now, working with a virtual environment is highly recommended. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP** - In the terminal/cmd, naviagte to the `/backend` directory and run:
```bash
pip install -r requirements.txt
```
to install all of the required packages in the `requirements.txt` file.


### Testing the API

To test the API you need to run the tests in the `test_flaskr.py` file. To do so, execute the following commands in your terminal:
```bash
dropdb trivia_test
```
```bash
createdb trivia_test
```
```bash
psql trivia_test < trivia.psql
```
```bash
python test_flaskr.py
```

### API keys

Currently the API can only be used locally. No API keys needed/provided.

## Error handling

Errors are returned in json format, e.g
```
{
  "success": "False",
  "error": 404,
  "message": "Not found error",
}
```

The error codes returned by the API include:
- 400 – Bad request error
- 404 – Not found error
- 422 – Unprocessable entity error
- 500 – Internal server error

## Endpoints

### GET /categories

**General**
- Returns all the question categories
- Example: `curl http://127.0.0.1:5000/categories`
```
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

### GET /questions

**General**
- Returns all the question, paginated in the format of 10 questions per page. Pages could be queried by a query string
- Example: `curl http://127.0.0.1:5000/questions?page=2`
```
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
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
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
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 25,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
```

### DELETE /questions/int:id

**General**
- Deletes a question with the specified id in the url
- Example: `curl -X DELETE http://127.0.0.1:5000/questions/6`
```
{
  "success": true
}
```

### POST /questions

**General**
- Creates a new question and adds it to the database
- Example: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{ "question": "Who was the president of Kenya in the year 2020?", "answer": "Uhuru Kenyatta", "difficulty": 2, "category": "4" }'`
```
{
  "success": true
}
```

### POST /search/questions

**General**
- Searches for questions containing the passed substring and returns the questions found
- Example: `curl -X POST http://127.0.0.1:5000/search/questions -H "Content-Type: application/json" -d '{"searchTerm": "1930"}'`
```
{
  "questions": [
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### GET /categories/int:id/questions

**General**
- Gets questions based on the category specified in the category id passed in the url
- Example: `curl http://127.0.0.1:5000/categories/6/questions`
```
{
  "current_category": "Sports",
  "questions": [
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
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### POST /quizzes

**General**
- Takes the category and previous questions' ids from the request and returns a random question which has not been asked yet
- Example: `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "History", "id": "4"}}'`
```
{
  "question": {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 25,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  "success": true
}
```
