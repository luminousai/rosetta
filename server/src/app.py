import logging

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd

from .convert import xlsx_to_jvfdtm


logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/convert")
async def convert(file: UploadFile):
    contents = await file.read()
    df = pd.read_excel(contents, header=None)
    xlsx_to_jvfdtm(df)

    return {"ok": "ok"}
