import fastapi
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import uvicorn

from datetime import datetime

api = FastAPI()

@api.get('/search/{article}', response_class=HTMLResponse)
def search(article : str):
    pass