import uvicorn

from fastapi import FastAPI

from v1.routes import router

app = FastAPI()

app.include_router(router, prefix="/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
