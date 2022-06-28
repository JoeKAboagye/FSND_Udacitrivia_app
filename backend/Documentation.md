# API DOCUMENTATION

## Getting Started

The API run locally at the default address `https://localhost:5000`

Authentication: This version does not require any form of authentication at this level.

## Error Handling

Errors are returned as JSON objects in this format:

```

{
    'Success': 'False',
    'error': 404,
    'message': 'resource not found'
}

```

You will receive errors of three types which include:
404: Resource not found
400: Bad request
422: Unproccesable
405: Method not allowed
500: Internal server error

## Endpoint Library

### Endpoints

GET /categories
GET /questions
DELETE /questions/{question_id}
POST /questions
POST /questions/search
GET /categories/{category_id}/questions
POST /quizzes

### GET /categories

- General

  - Fetches a dictionary of all categories of questions in the database.
  - Request arguments: None
  - Returns an object with a single key, 'categories' that contains an object of all the categories with id as key and the category as value.

- Sample Request
  Here is an example request:
  `curl http://localhost:5000/categories`

The above request will give the following response:

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

- General

  - Fetches all the questions in the database and paginates them into a group of 10 questions per page.
  - Request arguments:
    - Key: page(Alerts the API on the page of questions to render)
  - Returns an object containing:
    - a list of questions
    - number of total questions
    - all categories

- Sample request
  Here is an example request:

  `curl http://localhost:5000/questions?page=2`

The above request will give the following response:

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
              "id": 23,
              "question": "Which dung beetle was worshipped by the ancient Egyptians?"
            },
            {
              "answer": "Water",
              "category": 1,
              "difficulty": 3,
              "id": 24,
              "question": "What is H2O?"
            },
            {
              "answer": "Lionel Messi",
              "category": 6,
              "difficulty": 2,
              "id": 26,
              "question": "Who is the greatest player of all time?"
            },
            {
              "answer": "Nnamdi Azikiwe",
              "category": 4,
              "difficulty": 3,
              "id": 27,
              "question": "Who was the first President of Nigeria?"
            }
          ],
          "success": true,
          "total_questions": 20
        }

```

### DELETE /questions/{question_id}

- General

  - This deletes a specific question from our list of questions in the database.
  - Request Arguments:
    - Key: page(Alerts the API on the page of questions to render)
  - Returns an object containing
    - the deleted question ID
    - the questions left in the database
    - the total number of questions

- Sample request
  Here is an example request:
  `curl -X DELETE http://localhost:5000/questions/15`

The above request will give the following response:

```
      {
        "deleted": 15,
        "questions": [
          {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
          },
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
          }
        ],
        "success": true,
        "total_questions": 19
      }

```

### POST /questions

- General

  - Receives JSON data from the request and uses this data to insert a new question to the database.
  - Request arguments: None
  - Returns an object containing:
    - the created question ID
    - the total number of questions

- Sample Request
  Here is an example request:
  `curl -X POST -H "Content-Type: application/json" -d '{"answer": "Water", "question": "What is H2O?", "difficulty": 5, "category": 1}' http://localhost:5000/questions`

The above request will give the following response:

```
     {
        "created": 28,
        "success": true,
        "total_questions": 20
      }

```

### POST /questions/search

- General

  - Receives JSON data from the request and uses this data to search for a question containing the entered string.
  - Request arguments:
    - Key: page(Alerts the API on the page of questions to render)
  - Returns an object containing:
    - the questions containing that parameter
    - the total number of questions

- Sample Request
  Here is an example request:
  `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://localhost:5000/questions/search`

The above request will give the following response:

```
     {
        "questions": [
          {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
          }
        ],
        "success": true,
        "total_questions": 1
      }

```

### GET /categories/{category_id}/questions

- General

  - Fetches questions by category
  - Request arguments:
    - Key: page(Alerts the API on the page of questions to render)
  - Returns an object containing:
    - the questions in the requested category
    - the number of questions in that category
    - all categories
    - the current category

- Sample Request
  Here is an example request:
  `curl http://localhost:5000/categories/3/questions`

The above request will give the following response:

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
        "current_category": 3,
        "questions": [
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
          }
        ],
        "success": true,
        "total_questions": 2
      }

```

### POST /quizzes

- General

  - Receives JSON data from the request and uses this data to play a quiz game. The data received is the quiz category and the previous questions. The API returns a random question from that category that is not included in the previous questions.
  - Request arguments: None
  - Returns an object containing:
    - the generated question

- Sample Request
  Here is an example request:
  `curl -X POST -H "Content-Type: application/json" -d '{"quiz_category": 2, "previous_questions": [16, 17]}' http://localhost:5000/quizzes`

The above request will give the following response:

```
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
