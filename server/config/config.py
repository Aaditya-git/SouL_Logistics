import os

class Config:
    POSTGRES_URI = os.environ.get(
        'POSTGRES_URI', 
        'dbname=logistics user=postgres password=postgres host=localhost port=5433'
    )
