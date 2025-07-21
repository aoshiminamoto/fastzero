import uvicorn

from fastapi import FastAPI

from fastzero.routers import auth, todo, users

app = FastAPI(title="FastFromZero")

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(
        port=8000,
        reload=True,
        host="0.0.0.0",
        access_log=True,
        log_level="info",
        app="fastzero.app:app"
    )
