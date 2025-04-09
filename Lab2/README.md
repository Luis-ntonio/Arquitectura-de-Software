# **Kuadra - Parking Spot Rental (POC)**

Kuadra is a **proof-of-concept** application built with **FastAPI** that simulates the process of renting parking spots. It includes key features such as user and owner registration, parking spot reservations, and simple payment simulation.

---

## **Features**

- **User and Owner Registration**: Users and owners can register and manage their profiles.
- **Login**: Authentication system for user and owner access.
- **Search for Parking Spots (Cocheras)**: Find available parking spots based on location and other filters.
- **Manage Cocheras**: Owners can manage parking spots, including CRUD operations.
- **Reserve Cocheras**: Users can reserve available parking spots.
- **Simple Payment Simulation**: Simulate the payment process for parking spot rentals.
- **Reviews**: Users can leave reviews for cocheras they've rented.

---

## **Project Structure**

The project is organized into the following main sections:

1. **Authentication**: Handles user and owner registration and login.
2. **Parking Spot Management**: CRUD operations for managing parking spots by owners.
3. **Reservation System**: Allows users to search, reserve, and view parking spots.
4. **Payment Simulation**: Simple API for processing payment for reservations.
5. **Review System**: Users can review parking spots after renting them.

---

## **Requirements**

Before running the application, ensure you have the following installed:

- **Python 3.8+**: The required Python version for this project.
- **FastAPI**: For building the API.
- **uvicorn**: ASGI server to run the app.
- **pytest**: For running tests to verify functionality.

---

## **Setup**

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/kuadra.git
cd kuadra
```

### 2. **Create and Activate a Virtual Environment**

- **On Linux/Mac**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **On Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. **Install Dependencies**

Once the virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 4. **Run the Application**

Run the FastAPI application using `uvicorn`:

```bash
uvicorn main:app --reload
```

The API will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000). You can view the interactive API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 5. **Run Tests**

To ensure everything is working as expected, run the tests:

```bash
pytest
```

---

## **Endpoints Overview**

### **Authentication**

1. **POST** `/auth/login`
   - **Description**: Logs in a user or owner with their credentials.
   - **Returns**: Success or failure message.

### **Cocheras (Parking Spots)**

2. **GET** `/cocheras`
   - **Description**: Lists all available parking spots.
3. **POST** `/cocheras`
   - **Description**: Allows owners to create or manage a parking spot.
4. **GET** `/cocheras/{id}`
   - **Description**: Get details for a specific parking spot by ID.

### **Reservations**

5. **POST** `/reservations`
   - **Description**: Create a new parking spot reservation.
6. **GET** `/reservations/{id}`
   - **Description**: Get details of a specific reservation.

### **Payments**

7. **POST** `/payments`
   - **Description**: Simulates payment for a parking spot reservation.

---

## **Usage and Maintenance**

- **Stopping the App**: Simply press `Ctrl+C` to stop the `uvicorn` server.
- **Updating the Application**: After making changes, don't forget to restart the server with `uvicorn main:app --reload`.

---

## **Contributing**

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Push your changes to your fork.
5. Submit a pull request.

---