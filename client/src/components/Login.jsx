import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    MDBBtn,
    MDBContainer,
    MDBRow,
    MDBCol,
    MDBCard,
    MDBCardBody,
    MDBInput
} from 'mdb-react-ui-kit';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        const credentials = { email, password };
    
        try {
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            });
    
            if (response.ok) {
                const data = await response.json();
                
                if (data && data.id) {
                    navigate('/dashboard');
                } else {
                    alert('Login successful, but user ID is missing.');
                }
            } else {
                const error = await response.json();
                alert(`Error: ${error.detail}`);
            }
        } catch (err) {
            console.error('Error:', err);
            alert('Failed to login.');
        }
    };

    return (
        <MDBContainer fluid>
            <MDBRow className='d-flex justify-content-center align-items-center h-100'>
                <MDBCol col='12'>
                    <MDBCard className='bg-dark text-white my-5 mx-auto' style={{ borderRadius: '1rem', maxWidth: '600px' }}>
                        <MDBCardBody className='p-5 d-flex flex-column align-items-center mx-auto w-100'>
                            <h5>Welcome to</h5>
                            <h1 className="fw-bold mb-3">Soul Logistics</h1>
                            <p className="text-white-50 my-4">Please enter your email address and password!</p>

                            <MDBInput
                                wrapperClass='mb-4 mx-5 w-80'
                                labelClass='text-white'
                                label='Email address'
                                id='email'
                                type='email'
                                size="lg"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                            <MDBInput
                                wrapperClass='mb-4 mx-5 w-80'
                                labelClass='text-white'
                                label='Password'
                                id='password'
                                type='password'
                                size="lg"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />

                            <MDBBtn outline className='mx-2 my-4 px-5' color='white' size='lg' onClick={handleLogin}>
                                Login
                            </MDBBtn>
                        </MDBCardBody>
                    </MDBCard>
                </MDBCol>
            </MDBRow>
        </MDBContainer>
    );
}

export default Login;