from fastapi import FastAPI

app = FastAPI(title="CertMS")


@app.get("/")
def read_root():
    return {"Hello": "world"}
