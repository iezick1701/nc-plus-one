from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from db.connection import get_connection

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