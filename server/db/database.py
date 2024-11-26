import psycopg2
from psycopg2.extensions import connection as Connection
from server.config.config import Config

def get_db_connection() -> Connection:
    """
    Establish a connection to the PostgreSQL database.
    """
    return psycopg2.connect(Config.POSTGRES_URI)

def create_tables():
    """
    Create required tables in the PostgreSQL database.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                weight REAL NOT NULL,
                path TEXT[],
                status TEXT
            );

            CREATE TABLE IF NOT EXISTS tracking (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders (id),
                current_node TEXT,
                current_status TEXT,
                estimated_delivery TIMESTAMP,
                path TEXT[]
            );
            """)
            conn.commit()
  