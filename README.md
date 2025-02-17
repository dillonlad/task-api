# TaskAPI
This is a RESTful API built with FastAPI for managing tasks. It allows users to create, retrieve, update, and delete tasks.
## Features

Create a new task

Retrieve all tasks (with optional filters)

Retrieve a specific task

Update a task

Delete a task

## Running the project
This project can be set up and run through docker. For ease of use, you can download Docker Desktop here: https://www.docker.com/products/docker-desktop/. For Windows users, this will also install Windows Subsystem for Linux (WSL).
### Building Docker image
 Once you have docker set up on your local machine, open a command prompt or shell and navigate to the project folder, then type the following command:

`docker build -t task-api .`

Once done, you will have built a Docker Image for the project. The Dockerfile installation will install all of the required packages specified in requirements.txt

### Running docker container
Now that the image is built, you should create an api.env file in the project directory. You can use this to configure various project environment variables, such as the DEBUG env var. 

The only required environment variable is the DB_URL. Currently we are using a sqlite database and the value of this environment variable should be: `sqlite:////app/task_api.db`. This can be modified in the future to accomodate any database type (e.g. MySQL). The database included in this repository already has the necessary tables created, but a new database can be created using the schema defined in database/schema.sql.

Your api.env file should look like this:
```
db_url=sqlite:////app/task_api.db
```

This env file will not be included in any git commits.

After configuring the api.env file, run the following command:

`docker run -p 8000:8000  --env-file api.env task-api`

This will run the built Docker Image in a container on the port 8000. 

Once running, you can view the API documentation in any browser at `/redoc` e.g. `http://127.0.0.1:8000/redoc`. 

### API Endpoints

**Create a Task**

Endpoint: POST /tasks/

Request Body:
```
{
    "title": "Task Title",
    "description": "Task Description",
    "priority": 1,
    "due_date": "2000-01-30T15:00:00"
}
```
Response:
```
{
    "id": 1,
    "title": "Task Title",
    "description": "Task Description",
    "priority": 1,
    "due_date": "2000-01-30T15:00:00",
    "completed": false
}
```
**Retrieve All Tasks**

Endpoint: GET /tasks/

Query Parameters (Optional):

`completed (bool): Filter by completion status`

`priority (int): Filter by task priority`

Response:
```
[
    {
        "id": 1,
        "title": "Task Title",
        "description": "Task Description",
        "priority": 1,
        "due_date": "2000-01-30T15:00:00",
        "completed": false
    }
]
```
**Retrieve a Specific Task**

Endpoint: GET /tasks/{task_id}/

Response:
```
{
    "id": 1,
    "title": "Task Title",
    "description": "Task Description",
    "priority": 1,
    "due_date": "2000-01-30T15:00:00",
    "completed": false
}
```
**Update a Task**

Endpoint: PUT /tasks/{task_id}/

Request Body (All fields optional):
```
{
    "title": "Updated Task Title",
    "description": "Updated Task Description",
    "priority": 2,
    "due_date": "2000-02-01T15:00:00",
    "completed": true
}
```
Response:
```
{
    "id": 1,
    "title": "Updated Task Title",
    "description": "Updated Task Description",
    "priority": 2,
    "due_date": "2000-02-01T15:00:00",
    "completed": true
}
```
**Delete a Task**

Endpoint: DELETE /tasks/{task_id}/

Response:
```
{"message": "Task deleted successfully."}
```
## Testing the project
You can build and run a separate test Image which will have pytest installed and will run a suite of tests specified in the test/ directory.
### Building pytest image
`docker build -t task-api-test -f pytest_Dockerfile .`

### Running pytest image
Please create another .env file, separate to the api.env for specific use with pytest. With this you can specify a separate database.
`docker run --env-file test_api.env task-api-test`