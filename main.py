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