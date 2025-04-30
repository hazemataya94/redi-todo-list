from src.user import User
from src.todo_list import TodoList
from src.task import Task

from src.schemas import User as UserSchema
from src.schemas import TodoList as TodoListSchema
from src.schemas import Task as TaskSchema

from typing import List
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Routes
@app.post("/users/", response_model=UserSchema)
async def create_user(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    user = User(username=username, password=password)
    try:
        user.save()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": user.id,
        "username": user.username
    }
    
@app.get("/users/", response_model=List[UserSchema])
async def read_users():
    users = User.get_all()
    return users


@app.post("/todo_lists/", response_model=TodoListSchema)
async def create_todo_list(request: Request):
    data = await request.json()
    title = data.get("title")
    user_id = data.get("user_id")
    
    todo_list = TodoList(title=title, user_id=user_id)
    try:
        todo_list.save()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return todo_list

@app.get("/todo_lists/", response_model=List[TodoListSchema])
async def read_todo_lists():
    todo_lists = TodoList.get_all()
    return todo_lists

@app.post("/tasks/", response_model=TaskSchema)
async def create_task_for_todo_list(request: Request):
    data = await request.json()
    todo_list_id = data.get("todo_list_id")
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    
    task = Task(title=title, description=description, status=status, todo_list_id=todo_list_id)
    try:
        task.save()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return task
    
@app.get("/tasks/", response_model=List[TaskSchema])
async def read_tasks():
    tasks = Task.get_all()
    return tasks

@app.get("/todo_lists/{todo_list_id}/tasks/", response_model=List[TaskSchema])
async def read_tasks_for_todo_list(todo_list_id: int):
    tasks = Task.get_all(todo_list_id)
    return tasks
