from fastapi import APIRouter, Request
from core.database import LegacyDBHandler

router = APIRouter()
db = LegacyDBHandler("users.db")

from pydantic import BaseModel

class UserSearch(BaseModel):
    username: str

@router.get("/user/search")
def search_users(request: Request, username: str):
    """
    Search for users by username.
    """
    # FIXED: Use parameterized query
    query = "SELECT * FROM users WHERE username = ? AND active = 1"
    params = (username,)
    
    try:
        results = db.run_query_v2(query, params)
        return {"count": len(results), "users": results}
    except Exception as e:
        return {"error": str(e)}

@router.put("/user/{user_id}")
def update_user(user_id: int, user: UserSearch):
    query = "UPDATE users SET username = ? WHERE id = ?"
    params = (user.username, user_id)
    db.run_query_v2(query, params)
    return {"status": "updated"}

@router.delete("/user/{user_id}")
def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = ?"
    params = (user_id,)
    db.run_query_v2(query, params)
    return {"status": "deleted"}