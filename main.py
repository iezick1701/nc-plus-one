from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from db.connection import get_connection
from pydantic import BaseModel
from db.password import check_pwd
from db.token import create_access_token
from fastapi.responses import JSONResponse
from db.password import hash_pwd
import jwt

app = FastAPI(title="NC Plus One API", debug=True)


@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
@app.get("/api/events")
def get_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events ORDER BY starts_at ASC")
    events = cursor.fetchall()

    event_list = []

    for event in events:
        event_list.append({
            "id": event[0],
            "title": event[1],
            "description": event[2],
            "starts_at": event[3],
            "ends_at": event[4]
        })
    cursor.close()
    conn.close()
    return {"events": event_list}

@app.get("/api/events/{id}")
def get_event_by_id(id: str):
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Incorrect input")  
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events JOIN venues on events.venue_id = venues.id WHERE events.id = %s",(id,))
    event = cursor.fetchone()
    if event is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")


    event_dict = {
                "id": event[0],
                "title": event[1],
                "description": event[2],
                "starts_at": event[3],
                "ends_at": event[4],
                "location":event[9],
                "address":event[10],
                "capacity":event[11],
                "created_at":event[7]
            }
    cursor.close()
    conn.close()
    return {"event":event_dict}

class LoginRequest(BaseModel):
    email: str
    password: str
    
class CreateUser(BaseModel):
    email:str
    password: str
    name: str

@app.exception_handler(RequestValidationError)
def check_cred(request: Request, exc: RequestValidationError):
    if request.url.path == "/api/auth/login" :
        return JSONResponse(content ={"error":"Invalid login request"}, status_code=400)
    if request.url.path == "/api/auth/register" :
        return JSONResponse(content ={"error":"Invalid register request"}, status_code=400)
    
    return JSONResponse(content ={"error":exc.errors()}, status_code=422)
        



@app.post("/api/auth/login")
def check_login_cred(user:LoginRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (user.email,)
            )
    found_user = cursor.fetchone()
    if found_user is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    pwd = found_user[2]
    if check_pwd(user.password,pwd) is False:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    cursor.close()
    conn.close()
    
    token = create_access_token(found_user[0])
    return {"token":token}


@app.post("/api/auth/register",status_code=201)
def check_login_cred(user:CreateUser):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
    "SELECT email FROM users WHERE email = %s",
    (user.email,)
        )

    existing_user = cursor.fetchone()

    if existing_user is not None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=409, detail="Email already registered")
    cursor.execute("""
        INSERT INTO users (email,password,name)
        VALUES (%s,%s,%s)
        RETURNING id,created_at;
        """,
        (user.email,hash_pwd(user.password),user.name)
        
            )
    created_user = cursor.fetchone()
        
    
    cursor.close()
    conn.commit()
    conn.close()
    return {"user":{"id":created_user[0],
                    "name":user.name,
                    "email":user.email,
                    "created_at":created_user[1]
                    }}

    
    
    

    



