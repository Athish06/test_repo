from fastapi import APIRouter
from core.system import TaskRunner

router = APIRouter()
runner = TaskRunner("prod")

from fastapi import UploadFile, File
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@router.post("/images/convert")
def convert_image(filename: str, format: str):
    # FIXED: Sanitize filename and use safe command
    import re
    if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
        return {"error": "Invalid filename"}
    if format not in ['jpg', 'png', 'gif']:
        return {"error": "Invalid format"}
    
    cmd = f"convert uploads/{filename} output.{format}"
    # Assuming convert is safe now with sanitized input
    stdout, stderr = runner.execute_background_task(cmd)
    
    return {"status": "converted", "log": stdout}

def cleanup_old_files():
    for file in os.listdir(UPLOAD_DIR):
        if file.endswith(".tmp"):
            os.remove(os.path.join(UPLOAD_DIR, file))