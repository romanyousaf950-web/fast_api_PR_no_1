
from fastapi import FastAPI
from routers.users import router as users_router
from config import APP_NAME, DEBUG

# Create FastAPI App
app = FastAPI(
    title=APP_NAME,
    debug=DEBUG
)

# Connect User APIs
app.include_router(users_router)

@app.get("/")
def home():
    return {
        "message": "User Management API is running successfully",
        "app_name": APP_NAME,
        "developer": "Python Backend Developer"
    }

@app.get("/about")
def about():
    return {
        "message": "This is a FastAPI User Management Project"
    }
