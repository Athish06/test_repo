from fastapi import FastAPI
from api import auth, users, legacy, files

app = FastAPI(title="Vulnera App")

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(legacy.router, prefix="/legacy")
app.include_router(files.router, prefix="/files")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)