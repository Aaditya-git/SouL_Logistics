from fastapi import FastAPI, HTTPException
from db.database import get_db_connection
from utils.util import route
from typing import Dict
 
app = FastAPI()

@app.post('/order/add')
def add_order(order_data: Dict):
    """
    Add an order to the system, including route and tracking details.
    """
    origin = order_data['origin']
    destination = order_data['destination']
    
    try:
        # Calculate the actual route using osmnx
        path, status = route(origin, destination)
        delivery_times = calculate_estimated_delivery_time(path)

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Insert order into the orders table
                cursor.execute(
                    """
                    INSERT INTO orders (origin, destination, weight, path, status)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (origin, destination, order_data['weight'], path, 'New')
                )
                order_id = cursor.fetchone()[0]

                # Insert tracking data into the tracking table
                cursor.execute(
                    """
                    INSERT INTO tracking (order_id, current_node, current_status, estimated_delivery, path)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (order_id, path[0], 'New', delivery_times[path[-1]], path)
                )

                conn.commit()

        return {'order_id': order_id}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
