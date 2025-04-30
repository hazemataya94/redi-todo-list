from user import User
from todo_list import TodoList
from task import Task
from typing import List
from fastapi import FastAPI

app = FastAPI()

# Routes
@app.post("/users/", response_model=User)
def create_user(username: str, password: str):
    # user = User.create(username, password)
    
    user = User(username=username, password=password)
    user.save()
    
    return user

@app.post("/todo_lists/", response_model=TodoList)
def create_todo_list(title: str, user_id: int):
    todo_list = TodoList(title=title, user_id=user_id)
    todo_list.save()
    return todo_list

@app.get("/todo_lists/", response_model=List[TodoList])
def read_todo_list():
    todo_lists = TodoList.get_all()
    return todo_lists

@app.post("/todo_lists/{todo_list_id}/tasks/", response_model=Task)
def create_task_for_todo_list(todo_list_id: int, title: str, description: str, status: str):
    
    task = Task(title=title, description=description, status=status, todo_list_id=todo_list_id)
    task.save()
    return task
    
@app.get("/todo_lists/{todo_list_id}/tasks/", response_model=List[Task])
def read_tasks(todo_list_id: int):
    tasks = Task.get_all(todo_list_id)
    return tasks