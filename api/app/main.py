from fastapi import FastAPI

app = FastAPI(title="CertMS")


@app.get("/")
def root():
    return {"Hello": "World"}
