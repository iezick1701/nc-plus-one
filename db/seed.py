from db.connection import get_connection
import json 

def seed_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""CREATE TABLE users (id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    email VARCHAR(255) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    created_at TIMESTAMPTZ DEFAULT NOW()
    )
    
    """)
    data  = read_file('users')
    for user in data:
        cursor.execute("""
            INSERT INTO users (email, password, name)
                VALUES (%s, %s, %s);
            """,
            ( user["email"], user["password"], user["name"])
        )
    conn.commit()
    conn.close()


    pass


def read_file(file):
    with open(f"db/data/{file}.json","r") as f:
        data = json.load(f)
    return data


read_file("users")



def seed():

    seed_users()


seed()


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
