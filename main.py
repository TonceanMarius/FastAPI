<<<<<<< HEAD
from AI_functions import chatgpt, dalle
from sqlalchemy_db import SessionLocal, engine, User
from schema import UserSchema, UserResponseSchema
from fastapi import FastAPI, Depends, HTTPException
from typing import List
import requests
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    return {"Message": "Welcome to my API"}

@app.post("/generate_image")
async def generate_images(data: UserSchema, db: Session = Depends(get_db)):

    image_url = dalle(data.description)
    user = User(description = data.description, image_url = image_url)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@app.get("/images", response_model = List[UserResponseSchema])
async def get_images(db: Session = Depends(get_db)):
    images = db.query(User).all()
    return images

@app.delete("/delete_image")
async def delete_images(data: UserSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.description == data.description).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "Image not found")

    db.delete(user)
    db.commit()

    return user

@app.delete("/truncate")
async def truncate_table(db: Session = Depends(get_db)):

    images = db.query(User).delete()
    
    db.commit()

    return {"message":"Images deleted succeessfully!"}

@app.put("/update_image")
async def update_images(data: UserSchema, db: Session = Depends(get_db)):

    image = db.query(User).filter(User.id == data.id).first()

    if not image:
        raise HTTPException(status_code = "404", detail = "Image not found")

    image_url = dalle(data.description)
    new_image = User(description = data.description, image_url = image_url)

    image.description = new_image.description
    image.image_url = image_url

    db.commit()
    db.refresh(image)

    return image

@app.post("/smart_choice")
async def smart_choice(data: UserSchema, db: Session = Depends(get_db)):
    
    refined_prompt = chatgpt(data.description)
    if refined_prompt:
        url = dalle(refined_prompt)

    image = User(description = refined_prompt, image_url = url)

    db.add(image)
    db.commit()
    db.refresh(image)

    return image



if __name__ == "__main__":

    uvicorn.run(app, host = "127.0.0.1", port = 8001)
    refined_prompt = chatgpt()
    if refined_prompt:
        dalle(refined_prompt)
=======
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Task(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks = []

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task


@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[idx] = updated_task
            return updated_task
        
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)
    
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
>>>>>>> 85e3e08ecf9747716133ec334aaf8a704d1fd353
