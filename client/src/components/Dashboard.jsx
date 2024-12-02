import React, { useState } from 'react';
import { TabMenu } from 'primereact/tabmenu';
import Orders from './Orders';
import Products from './Products';
import Container from 'react-bootstrap/Container';
import 'primereact/resources/themes/md-light-deeppurple/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

function Dashboard() {
    const [activeIndex, setActiveIndex] = useState(0);

    const items = [
        { label: 'Orders', icon: 'pi pi-box' },
        { label: 'Tracking', icon: 'pi pi-map' },
        { label: 'Products', icon: 'pi pi-list' }
    ];

    const renderContent = () => {
        switch (activeIndex) {
            case 0:
                return <Orders />;
            case 1:
                return <>Tracking</>;
            case 2:
                return <Products />;
            default:
                return <div><h2>Welcome</h2><p>Select a tab to get started.</p></div>;
        }
    };

    return (
        <Container>
            <TabMenu 
                model={items} 
                activeIndex={activeIndex} 
                onTabChange={(e) => setActiveIndex(e.index)} 
            />
            <div style={{ marginTop: '20px' }}>
                {renderContent()}
            </div>
        </Container>
    );
}

export default Dashboard;