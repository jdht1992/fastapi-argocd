from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "¡Hola desde Kubernetes!", "status": "Ready"}


@app.get("/health")
def health_check():
    return {"status": "Healthy"}