from fastapi import FastAPI 

app = FastAPI(
    title="Google Calender Salary Calculator",
    version="1.0.0"
)

@app.get("/")
def reaf_root():
    return {
        "status":"online",
        "message": "FastAPI backend is up and running!"
    }
