# from pydantic import BaseModel

# class User(BaseModel):
#     id: int
#     name: str



# Create User API:
# @app.post("/users")
# def create_user(user: User):
#     users.append(user.dict())
#     return {"message": "User created", "user": user}



# Get All Users:
# @app.get("/users")
# def get_users():
#     return users


# 👉 Call:

# GET /users


# 📌 Output:

# [
#  {"id":1,"name":"Lalit"},
#  {"id":2,"name":"Rahul"}
# ]

# Get Single User (Path Param)
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     for user in users:
#         if user["id"] == user_id:
#             return user
#     return {"error": "User not found"}


# 👉 Example:

# # GET /users/1










# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# # fake DB
# users = [
#     {"id": 1, "name": "Lalit"},
#     {"id": 2, "name": "Rahul"}
# ]


# class User(BaseModel):
#     id: int
#     name: str

# ✅ GET – get all users
# @app.get("/users")
# def get_users():
#     return users

# ✅ POST – add user
# @app.post("/users")
# def add_user(user: User):
#     users.append(user.dict())
#     return user

# ✅ PUT – update user
# @app.put("/users/{user_id}")
# def update_user(user_id: int, user: User):
#     for i, u in enumerate(users):
#         if u["id"] == user_id:
#             users[i] = user.dict()
#             return {"message": "Updated"}
#     return {"error": "User not found"}


# ✅ DELETE – remove user
# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     for u in users:
#         if u["id"] == user_id:
#             users.remove(u)
#             return {"message": "Deleted"}
#     return {"error": "User not found"}