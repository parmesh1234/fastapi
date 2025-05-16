from fastapi import FastAPI, Request
from .routers import auth, todos,admin, users

from .models import Base
from .database import engine

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="TODO_APP/templates")

app.mount("/static", StaticFiles(directory="TODO_APP/static"), name="static")


@app.get("/")
def test(request:Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get('/healthy')
async def health_check():
    return {'status':'we are good'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
