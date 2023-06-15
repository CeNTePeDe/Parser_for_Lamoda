from fastapi import FastAPI

app = FastAPI(
    title="Parser"
)


@app.get("/")
def main():
    return {"message": "Hello World"}
