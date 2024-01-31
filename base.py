import psycopg2


db = "banco"
user = "admin"
password = "123"
host = "localhost"
port = "5432"


conn = psycopg2.connect(f"dbname={db} user={user} password={password} host={host} port={port}")
# cur = conn.cursor()

# cur.execute(""" 
#     CREATE TABLE IF NOT EXISTS cuentas (
#         id SERIAL PRIMARY KEY,
#         saldo DECIMAL(10, 2) NOT NULL
#     )
# """)

# cur.commit