from fastapi import FastAPI
from controller.order_controller import app as logistics_app
import uvicorn
from db.database import create_tables

# Create tables in the database
create_tables()

app = FastAPI(title="Logistics Management System")
app.mount("/logistics", logistics_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
