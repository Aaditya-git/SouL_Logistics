import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import axios from 'axios';

export default function Orders() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await axios.get('http://localhost:8000/orders');
                setOrders(response.data);
            } catch (error) {
                console.error('Error fetching orders:', error);
            }
        };

        fetchOrders();
    }, []);

    return (
        <div className="card">
            <DataTable value={orders} removableSort tableStyle={{ minWidth: '50rem' }}>
                <Column field="_id" header="Tracking ID" sortable style={{ width: '25%' }}></Column>
                <Column field="product_id" header="Product" sortable style={{ width: '25%' }}></Column>
                <Column field="status" header="Status" sortable style={{ width: '15%' }}></Column>
                <Column field="quantity" header="Quantity" sortable style={{ width: '15%' }}></Column>
                <Column field="created_at" header="Order Placed" sortable style={{ width: '20%' }}></Column>
            </DataTable>
        </div>
    );
}