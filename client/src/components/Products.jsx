import React, { useState, useEffect } from 'react';
import { Button } from 'primereact/button';
import { DataView } from 'primereact/dataview';
import { Dropdown } from 'primereact/dropdown';
import { Tag } from 'primereact/tag';
import { classNames } from 'primereact/utils';
import axios from 'axios';

export default function Products() {
    const [products, setProducts] = useState([]);
    const [sortKey, setSortKey] = useState('');
    const [sortOrder, setSortOrder] = useState(0);
    const [sortField, setSortField] = useState('');
    const sortOptions = [
        { label: 'Price High to Low', value: '!price' },
        { label: 'Price Low to High', value: 'price' }
    ];

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await axios.get('http://localhost:8000/products');
                const transformedProducts = response.data.map((product) => ({
                    id: product._id,
                    name: product.name,
                    description: product.description,
                    price: product.price,
                    category: product.category,
                    inventoryStatus:
                        product.available_stock > 100
                            ? 'INSTOCK'
                            : product.available_stock > 0
                            ? 'LOWSTOCK'
                            : 'OUTOFSTOCK',
                    tags: product.tags.join(', '),
                    dimensions: `${product.dimensions.length}x${product.dimensions.width}x${product.dimensions.height}`,
                    availableStock: product.available_stock,
                    manufacturer: product.manufacturer,
                }));
                setProducts(transformedProducts);
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };

        fetchProducts();
    }, []);

    const getSeverity = (inventoryStatus) => {
        switch (inventoryStatus) {
            case 'INSTOCK':
                return 'success';
            case 'LOWSTOCK':
                return 'warning';
            case 'OUTOFSTOCK':
                return 'danger';
            default:
                return null;
        }
    };

    const onSortChange = (event) => {
        const value = event.value;

        if (value.indexOf('!') === 0) {
            setSortOrder(-1);
            setSortField(value.substring(1));
            setSortKey(value);
        } else {
            setSortOrder(1);
            setSortField(value);
            setSortKey(value);
        }
    };

    const handleAddToCart = async (productId) => {
        try {
            await axios.post('http://localhost:8000/placeOrder', { id: productId });
        } catch (error) {
            console.error('Error adding to cart:', error);
        }
    };

    const header = () => {
        return <Dropdown options={sortOptions} value={sortKey} optionLabel="label" placeholder="Sort By Price" onChange={onSortChange} className="w-full sm:w-14rem" />;
    };

    const itemTemplate = (product, index) => {
        return (
            <div className="col-12" key={product.id}>
                <div className={classNames('flex flex-column xl:flex-row xl:align-items-start p-4 gap-4', { 'border-top-1 surface-border': index !== 0 })}>
                    <div className="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-4">
                        <div className="flex flex-column align-items-center sm:align-items-start gap-3">
                            <div className="text-2xl font-bold text-900">{product.name}</div>
                            <div className="text-700">{product.description}</div>
                            <div className="flex align-items-center gap-3">
                                <span className="flex align-items-center gap-2">
                                    <i className="pi pi-tag"></i>
                                    <span className="font-semibold">{product.category} | {product.tags}</span>
                                </span>
                                <Tag value={product.inventoryStatus} severity={getSeverity(product.inventoryStatus)}></Tag>
                            </div>
                            <div className="text-600 text-sm">Manufacturer: {product.manufacturer}</div>
                        </div>
                        <div className="flex sm:flex-column align-items-center sm:align-items-end gap-3 sm:gap-2">
                            <span className="text-2xl font-semibold">${product.price}</span>
                            <Button 
                                icon="pi pi-shopping-cart" 
                                className="p-button-rounded" 
                                disabled={product.inventoryStatus === 'OUTOFSTOCK'}
                                onClick={() => handleAddToCart(product.id)}
                            ></Button>
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="card">
            <DataView
                value={products}
                itemTemplate={itemTemplate}
                header={header()}
                sortField={sortField}
                sortOrder={sortOrder}
            />
        </div>
    );
}
