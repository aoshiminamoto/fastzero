from fastapi import FastAPI

from fastzero.routers import auth, todo, users

app = FastAPI(title="FastFromZero")

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(users.router)
