from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.db.models.orders import Order
from app.routes import users, products, warehouse, inventory, orders, shipments
from app.db.database import *
from pydantic import BaseModel
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(warehouse.router, prefix="/api", tags=["Warehouse"])
app.include_router(inventory.router, prefix="/api", tags=["Inventory"])
app.include_router(orders.router, prefix="/api", tags=["Orders"])
app.include_router(shipments.router, prefix="/api", tags=["Shipments"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

class AddToCartRequest(BaseModel):
    id: str
    
class OrderStatus(BaseModel):
    order_id: str

SHARED_DATA = {
    'id': '',
    'region': ''
}

@app.get("/")
async def root():
    global SHARED_DATA
    SHARED_DATA['id'] = ''
    return {"message": "Welcome to the Logistics and Supply Chain Management API"}


@app.post("/login")
async def login(request: LoginRequest):
    global SHARED_DATA
    SHARED_DATA['id'], SHARED_DATA['region'] = await query_user_by_email(request.email)
    if SHARED_DATA['id'] and SHARED_DATA['region']:
        return {'id': SHARED_DATA['id']}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@app.get("/orders")
async def get_orders():
    global SHARED_DATA
    orders = await query_all_orders(SHARED_DATA['id'])
    for order in orders:
        product = await query_product(order['product_id'])
        order['product_id'] = product['name']
        dt_object = datetime.fromisoformat(order['created_at'])
        order['created_at'] = dt_object.strftime("%B %d, %Y")
    return orders


@app.get("/products")
async def get_products():
    global SHARED_DATA
    products = await query_all_products()
    return products


@app.post('/placeOrder', status_code=status.HTTP_201_CREATED)
async def place_order(id: AddToCartRequest):
    try:
        user_data = await query_user(SHARED_DATA['id'])

        payload = {
            'user_id': SHARED_DATA['id'],
            'product_id': id.id,
            'status': 'Processing',
            'address': user_data['address'],
            'city': user_data['city'],
            'state': user_data['state'],
            'zip_code': user_data['zip_code'],
            'region': SHARED_DATA['region'],
            'created_at': datetime.now().isoformat()
        }

        try:
            order_data = Order(**payload)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Validation error: {e}")

        order_dict = order_data.model_dump(by_alias=True)
        response = await insert_order(order_dict)
        if response:
            await update_shipment_status(response, order_dict['status'])
            return {"message": "Order placed successfully", "data": response}

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/orderStatus")
async def get_order_status(order_id: OrderStatus):
    order = await query_order(order_id.order_id)
    status_mappings = {'Placed': 0, 'Processing': 1, 'Shipped': 2, 'In Transit': 3, 'Delivered': 4}
    return {'index': status_mappings.get(order['status'])}
