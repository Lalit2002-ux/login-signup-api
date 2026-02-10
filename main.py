from fastapi import FastAPI, Form, HTTPException
from database import get_connection
from auth import hash_password, verify_password
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()


# tell FastAPI where HTML files are
templates = Jinja2Templates(directory="templates")

#  DEFAULT ROUTE → LOGIN PAGE
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/welcome", response_class=HTMLResponse)
def welcome_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


# @app.get("/login")
# def login_page():
#     return FileResponse("templates/login.html")

# @app.get("/signup")
# def signup_page():
#     return FileResponse("templates/signup.html")

# @app.get("/welcome")
# def home_page():
#     return FileResponse("templates/welcome.html")




@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # get user password hash
        cur.execute(
            # Executes a SQL query to retrieve the password hash for the user with the provided email address 
            # from the users table in the Snowflake database. The %s is a placeholder for the email variable, 
            # which is passed as a parameter to prevent SQL injection attacks.
            "SELECT username,password_hash FROM users WHERE email = %s",
            (email,)
        )

        result = cur.fetchone()

        if not result:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "User does not exist"}
            )
            # If no user is found with the provided email, it returns a JSON response with an error message 
            # and a 400 status code, indicating that the request was invalid due to the non-existent user.

        stored_hash = result[1]
        username = result[0]
        # Extracts the password hash from the query result, which is typically returned as a tuple. 
        # The password hash is expected to be in the first position of the tuple (index 0). 
        # This stored_hash will be used to verify the provided password against the stored hash in the database.

        # verify password
        if not verify_password(password, stored_hash):
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Invalid credentials"}
            )
            # If the provided password does not match the stored hash, it returns a JSON

        # login success response with a 401 status code, indicating that the request was unauthorized due to invalid credentials.
        return {
            "success": True,
            "user_name": username,
            "message": "Login successful"   
        }
        # If the password is verified successfully, it returns a JSON response indicating that the login 
        # was successful, along with the user's email address.

    finally:
        cur.close()
        conn.close()


@app.post("/signup")
def signup(
    username: str = Form(...),   # "..." means this field is required
    email: str = Form(...),      # Receives form data from browser,Converts it into Python variables,Ensures values are not empty
    password: str = Form(...)
):
    conn = get_connection()  # Calls database.py to establish connection with Snowflake
    cur = conn.cursor()      # Creates a cursor object to execute SQL queries on the Snowflake database

    try:
        # check user exists
        cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "User already exists"}
            )
            # Checks if a user with the provided email already exists in the database. 
            # If a user is found, it returns a JSON response with an error message and a 400 status code, 
            # indicating that the request was invalid due to the existing user.

        if len(password.encode("utf-8")) > 20:
            # Checks if the password length exceeds 5 bytes when encoded in UTF-8, which is a common encoding for text.
            # If the password is too long, it raises an HTTPException with a 400 status code and a message indicating that the password is too long.
            raise HTTPException(400, "Password too long")

        hashed_pwd = hash_password(password)  # Calls auth.py Converts password into secure hash

        cur.execute(
            # Inserts new user data into the users table in Snowflake database
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (username, email, hashed_pwd)
        )

        conn.commit()  # Commits the transaction to save changes to the database

        return {"success": True, "message": "User created successfully"}
        # Returns a JSON response indicating that the user was created successfully

    finally:
        # Closes the cursor and connection to free up resources after the operation is complete, regardless of success or failure
        cur.close()
        conn.close()


# @app.get("/getuser/{user_id}")
# Defines a GET endpoint that takes a user_id as a path parameter, retrieves the corresponding user information 
# from the database using the get_user function, and returns it as a JSON response. 
# If the user is not found, it raises an HTTPException with a 404 status code.
# def get_user(user_id: int):
#     conn = get_connection()
#     cur = conn.cursor()

#     try:
#         cur.execute(
#             "SELECT username, email FROM users WHERE id = %s",
#             (user_id,)
#         )
#         result = cur.fetchone()

#         if not result:
#             raise HTTPException(404, "User not found")

#         return {"username": result[0], "email": result[1]}

#     finally:
#         cur.close()
#         conn.close()


@app.get("/apitesting")
# Defines a GET endpoint at /endpoint that returns a simple JSON message, useful for testing if the API is running correctly
def home():
    return ["API IS WORKING PROPERLY!"]
