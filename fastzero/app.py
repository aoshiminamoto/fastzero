from fastapi import FastAPI

app = FastAPI(title="FastFromZero")


@app.get("/")
def read_root():
    return "Batatinhas Fritas Voadoras"
