import requests
import time

def simulate_user_flow():
    # 1. Register user
    print("Registering user...")
    r = requests.post("http://localhost:5001/register", json={"username": "pedro", "password": "123"})
    print(r.json())

    # 2. Login user
    print("Logging in user...")
    r = requests.post("http://localhost:5001/login", json={"username": "pedro", "password": "123"})
    print(r.json())

    # 3. List products
    print("Listing products...")
    r = requests.get("http://localhost:5002/products")
    products = r.json()
    print(products)

    # 4. Create order (this triggers event)
    print("Creating order...")
    r = requests.post("http://localhost:5003/order", json={"user": "pedro", "product_id": products[0]["id"]})
    print(r.json())

    # 5. Process payment
    print("Processing payment...")
    r = requests.post("http://localhost:5004/payment", json={"user": "pedro", "order_id": 1, "amount": 100})
    print(r.json())

    print("Wait a moment for notifications to be printed by notification_service...")

if __name__ == "__main__":
    simulate_user_flow()
    time.sleep(2)