from db.connection import get_connection
import json 
from db.password import hash_pwd

def seed_users(database=None, data_path="db/data/dev"):    
    conn = get_connection(database)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""CREATE TABLE users (id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    email VARCHAR(255) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    created_at TIMESTAMPTZ DEFAULT NOW()
    )
    
    """)
    data  = read_file('users',data_path)
    for user in data:
        cursor.execute("""
            INSERT INTO users ( email, password, name)
                VALUES (%s, %s, %s);
            """,
            ( user["email"], hash_pwd(user["password"]),user["name"])
        )
    conn.commit()
    conn.close()


    


def seed_venues(database=None, data_path="db/data/dev"):    
    conn = get_connection(database)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS venues")
    cursor.execute("""CREATE TABLE venues (id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    name VARCHAR(255)  NOT NULL, 
    address TEXT , 
    capacity INT 
    )
    
    """)
    data  = read_file('venues',data_path)
    for user in data:
        cursor.execute("""
            INSERT INTO venues (name, address, capacity)
                VALUES (%s, %s, %s);
            """,
            ( user["name"], user["address"], user["capacity"])
        )
    conn.commit()
    conn.close()


def seed_events(database=None, data_path="db/data/dev"):    
    conn = get_connection(database)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS events")

    cursor.execute("""
        CREATE TABLE events (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            starts_at TIMESTAMPTZ NOT NULL,
            ends_at TIMESTAMPTZ NOT NULL,
            organiser_id INT,
            venue_id INT,
            created_at TIMESTAMPTZ DEFAULT NOW(),

            CONSTRAINT fk_organiser
                FOREIGN KEY (organiser_id)
                REFERENCES users(id),

            CONSTRAINT fk_venue
                FOREIGN KEY (venue_id)
                REFERENCES venues(id)
        )
    """)

    data = read_file("events",data_path)

    for event in data:
        cursor.execute("""
            INSERT INTO events (
                title,
                description,
                starts_at,
                ends_at,
                organiser_id,
                venue_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            event["title"],event["description"],event["starts_at"],event["ends_at"],event["organiser_id"],event["venue_id"]
        ))

    conn.commit()
    conn.close()

    
    

def seed_rsvps(database=None, data_path="db/data/dev"):    
    conn = get_connection(database)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS rsvps")

    cursor.execute("""
        CREATE TABLE rsvps (
            id SERIAL PRIMARY KEY,
            attendee_id INT,
            event_id INT,
            created_at TIMESTAMPTZ DEFAULT NOW(),

            CONSTRAINT fk_attendee
                FOREIGN KEY (attendee_id)
                REFERENCES users(id),

            CONSTRAINT fk_event
                FOREIGN KEY (event_id)
                REFERENCES events(id)
        )
    """)

    data = read_file("rsvps",data_path)

    for rsvp in data:
        cursor.execute("""
            INSERT INTO rsvps (attendee_id, event_id)
            VALUES (%s, %s)
        """, (
            rsvp["attendee_id"],
            rsvp["event_id"]
        ))

    conn.commit()
    cursor.close()
    conn.close()

def read_file(file, data_path="db/data/dev"):
    with open(f"{data_path}/{file}.json", "r") as f:
        data = json.load(f)
    return data





def seed(database=None, data_path="db/data/dev"):
    conn = get_connection(database)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS rsvps")
    cursor.execute("DROP TABLE IF EXISTS events")

    conn.commit()
    cursor.close()
    conn.close()

    seed_users(database,data_path)
    seed_venues(database,data_path)
    seed_events(database,data_path)
    seed_rsvps(database,data_path)

def seed_test():
    seed("nc_plus_one_test","db/data/test")




if __name__ == "__main__":
    seed()
    seed_test()

# def show_table(table):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT column_name, data_type, is_nullable
#         FROM information_dicthema.columns
#         WHERE table_name = %s
#         ORDER BY ordinal_position
#     """,(table,))

#     for column in cursor.fetchall():
#         print(column)

#     conn.close()

# show_table("users")
