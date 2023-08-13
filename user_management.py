from fastapi import FastAPI, HTTPException, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: str
    name: str
    email: str
    password: str

users = []

@app.post("/add-user/")
async def add_user(user: User):
    users.append(user)
    return user

@app.put("/update-user/{user_id}")
async def update_user(user_id: str, updated_user: User):
    user_index = next((index for index, user in enumerate(users) if user.id == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_index] = updated_user
    return {"message": "User updated"}

@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
    user_index = next((index for index, user in enumerate(users) if user.id == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = users.pop(user_index)
    return {"message": "User deleted", "deleted_user": deleted_user}

@app.get("/users/", response_class=HTMLResponse)
async def list_users():
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

@app.post("/create-user/")
async def create_user(background_tasks: BackgroundTasks, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    user_id = str(uuid4())
    new_user = User(id=user_id, name=name, email=email, password=password)
    background_tasks.add_task(add_user, new_user)
    return {"message": "User creation in progress", "user_id": user_id}


@app.get("/")
async def read_root():
    return {"message": "Welcome to the User Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

