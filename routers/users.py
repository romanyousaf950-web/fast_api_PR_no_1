
from fastapi import APIRouter, HTTPException, Query

from database import get_db_connection
from schemas import User, UserUpdate

router = APIRouter()


# GET all users
@router.get("/users")
def get_users(
    min_age: int | None = Query(default=None, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    sort_by_age: bool = False
):
    conn = get_db_connection()

    query = "SELECT * FROM users"
    values = []

    if min_age is not None:
        query += " WHERE age >= ?"
        values.append(min_age)

    if sort_by_age:
        query += " ORDER BY age"

    query += " LIMIT ?"
    values.append(limit)

    users = conn.execute(query, values).fetchall()
    conn.close()

    return [dict(user) for user in users]


# GET single user
@router.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    conn.close()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(user)


# POST create user
@router.post("/users/{user_id}", status_code=201)
def create_user(user_id: int, user: User):
    conn = get_db_connection()

    existing = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(status_code=409, detail="User already exists")

    conn.execute(
        "INSERT INTO users (id, name, age) VALUES (?, ?, ?)",
        (user_id, user.name, user.age)
    )

    conn.commit()
    conn.close()

    return {"message": "User created successfully"}


# PUT update complete user
@router.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_db_connection()

    result = conn.execute(
        "UPDATE users SET name = ?, age = ? WHERE id = ?",
        (user.name, user.age, user_id)
    )

    conn.commit()
    conn.close()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully"}


# PATCH partially update user
@router.patch("/users/{user_id}")
def partial_update_user(user_id: int, user: UserUpdate):
    conn = get_db_connection()

    existing = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    data = user.model_dump(exclude_unset=True, exclude_none=True)

    if not data:
        conn.close()
        raise HTTPException(status_code=400, detail="No data provided")

    for key, value in data.items():
        conn.execute(
            f"UPDATE users SET {key} = ? WHERE id = ?",
            (value, user_id)
        )

    conn.commit()
    conn.close()

    return {"message": "User partially updated successfully"}


# DELETE user
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()

    result = conn.execute(
        "DELETE FROM users WHERE id = ?", (user_id,)
    )

    conn.commit()
    conn.close()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}
