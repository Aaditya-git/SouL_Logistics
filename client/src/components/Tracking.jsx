import React, { useState } from 'react'; 
import { Steps } from 'primereact/steps';
import { InputText } from "primereact/inputtext";
import { Button } from 'primereact/button';

export default function TemplateDemo() {
    const [activeIndex, setActiveIndex] = useState(0);
    const [value, setValue] = useState('');

    const itemRenderer = (item, itemIndex) => {
        const isActiveItem = activeIndex >= itemIndex;
        const backgroundColor = isActiveItem ? 'var(--primary-color)' : 'var(--surface-b)';
        const textColor = isActiveItem ? 'var(--surface-b)' : 'var(--text-color-secondary)';

        return (
            <div className="flex flex-column align-items-center">
                <span
                    className="inline-flex align-items-center justify-content-center border-circle border-primary border-1 h-3rem w-3rem z-1 cursor-pointer"
                    style={{ backgroundColor: backgroundColor, color: textColor }}
                >
                    <i className={`${item.icon} text-xl`} />
                </span>
                <span className="mt-2" style={{fontWeight: isActiveItem ? 'bold' : 'normal' }}>
                    {item.label}
                </span>
            </div>
        );
    };

    const handleInput = async () => {
        try {
            const response = await fetch('http://localhost:8000/orderStatus', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ order_id: value }),
            });

            if (response.ok) {
                const data = await response.json();
                setActiveIndex(data.index); // Set the active index based on backend response
            } else {
                const error = await response.json();
                alert(`Error: ${error.detail}`);
            }
        } catch (err) {
            console.error('Error:', err);
            alert('Failed to fetch status.');
        }
    };

    const items = [
        {
            label: 'Placed',
            icon: 'pi pi-user',
            template: (item) => itemRenderer(item, 0)
        },
        {
            label: 'Processing',
            icon: 'pi pi-spinner',
            template: (item) => itemRenderer(item, 1)
        },
        {
            label: 'Shipped',
            icon: 'pi pi-box',
            template: (item) => itemRenderer(item, 2)
        },
        {
            label: 'Transit',
            icon: 'pi pi-truck',
            template: (item) => itemRenderer(item, 3)
        },
        {
            label: 'Delivered',
            icon: 'pi pi-check',
            template: (item) => itemRenderer(item, 4)
        }
    ];

    return (
        <div className="card">
            <div className="p-inputgroup">
                <InputText 
                    value={value} 
                    onChange={(e) => setValue(e.target.value)} 
                    placeholder="Enter Order ID" 
                />
                <Button label="Search" icon="pi pi-search" onClick={handleInput} />
            </div>
            <Steps model={items} activeIndex={activeIndex} readOnly={true} className="mt-5 px-5" />
        </div>
    );
}
