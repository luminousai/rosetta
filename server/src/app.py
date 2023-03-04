from fastapi import FastAPI

from . import jvfdtm


app = FastAPI()


@app.get("/objects")
async def objects():
    return jvfdtm.Object.list()
