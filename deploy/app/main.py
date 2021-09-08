import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
from proj.celery import app
from proj.tasks import generator
from celery.result import AsyncResult


class Item(BaseModel):
    textprompt: str


fastapp = FastAPI()

fastapp.mount("/static", StaticFiles(directory="/build/app/static"), name="static")

templates = Jinja2Templates(directory="/build/app/templates")


@fastapp.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@fastapp.post("/generate")
async def run_generation(input: Item):
    task = generator.delay(input.textprompt)
    response = {"task_id": task.id}
    return json.dumps(response)


@fastapp.get("/generate/{task_id}")
async def run_generation_check(task_id: str):
    task = AsyncResult(task_id, app=app)
    response = {
        "state": task.state,
        "result": task.result
    }
    return json.dumps(response)