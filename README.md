# **Distributed Logistics Management System**

This application is designed to manage logistics efficiently using a distributed database system. It features a **React-based front end** and a **FastAPI-based backend**, with MongoDB as the database. Sensitive configurations, like MongoDB URIs, are securely managed using environment variables.

---

## **Features**
- **Frontend**: Built with React, offering a responsive and user-friendly interface.
- **Backend**: Powered by FastAPI, providing a robust API for data handling.
- **Database**: MongoDB for scalable and efficient storage.
- **Environment Configuration**: Sensitive information like database URIs is securely managed using `.env` files.

---

## **Getting Started**

### **1. Prerequisites**
Ensure you have the following installed:
- Node.js (v16 or later)
- Python (v3.8 or later)
- MongoDB (local or cloud-based)
- `pipenv` (for Python dependency management)

---

### **2. Installation**

#### **Backend Setup**
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
4. Install dependencies using requirements.txt
   ```bash
   pip3 install -r requirement.txt
5. Install react dependencies
   ```bash
   cd client
   npm install
6. Create a `.env` file and copy paste the data from `.env.example`
7. Paste your MongoDB connection string in front of `MONGO_URI`
8. Start frontend server
   ```bash
   cd client
   npm start
9. Start backend server
   ```bash
   cd ../
   uvicorn main:app --reload

---

### **3. Usage**
1. API Base URL: The backend runs on `http://localhost:8000` by default
2. Frontend URL: Access the application at `http://localhost:3000` in your browser
3. Environment Variable Handling: Make sure the `.env` file contains valid MongoDB connection strings

---

### **4. File Structure**
├── app/
│   ├── main.py
│   ├── db/
│   ├── routers/
│   ├── services/
│   ├── config.py
├── client/
│   ├── src/
│   │   ├── components/
│   │   └── App.js
│   ├── package.json
├── venv/
├── .env
├── .env.example
├── .gitignore
├── main.py
├── README.md
├── requirement.txt

