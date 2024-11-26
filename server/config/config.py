import os

class Config:
    POSTGRES_URI = os.environ.get(
        'POSTGRES_URI', 
        'dbname=logistics user=postgres password=password host=localhost port=5432'
    )
