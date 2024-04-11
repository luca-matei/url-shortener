import uvicorn

from fastapi import FastAPI

from v1.clients.redis import RedisSession

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
