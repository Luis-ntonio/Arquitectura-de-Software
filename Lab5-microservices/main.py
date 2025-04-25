import requests
import time

def simulate_user_flow():
    # 1. Register user
    print("Registering user...")
    r = requests.post("http://user_service:5001/register", json={"username": "pedro", "password": "123"})
    print(r.json())

    # 2. Login user
    print("Logging in user...")
    r = requests.post("http://user_service:5001/login", json={"username": "pedro", "password": "123"})
    print(r.json())

    # 3. List products
    print("Listing products...")
    r = requests.get("http://product_service:5002/products")
    products = r.json()
    print(products)

    # 4. Request product (instead of directly creating an order)
    print("Requesting product...")
    for _ in range(10):  # Simulate 300 requests to trigger the batch
        r = requests.post("http://request_service:5005/request_product", json={"product_id": products[0]["id"]})
        print(r.json())

    # 5. Wait for the order to be created automatically
    print("Waiting for the order to be created by request_service...")

    # 6. Process payment
    print("Processing payment...")
    r = requests.post("http://payment_service:5004/payment", json={"user": "pedro", "order_id": 1, "amount": 100})
    print(r.json())

    print("Wait a moment for notifications to be printed by notification_service...")

if __name__ == "__main__":
    simulate_user_flow()
    time.sleep(2)