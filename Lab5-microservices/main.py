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

    # 3. Check provider products directly
    print("Checking provider products...")
    r = requests.get("http://provider_service:5010/provider_products")
    provider_products = r.json()
    print(provider_products)

    # 4. List products through product service
    print("Listing products from product service...")
    r = requests.get("http://product_service:5002/products")
    products = r.json()
    print(products)

    # 5. Create an order directly
    print("Creating an order...")
    provider_id = 1  # Assuming provider ID 1
    product_id = products[0]["id"]
    r = requests.post("http://order_service:5003/order", json={"provider_id": provider_id, "product_id": product_id, "quantity": 2})
    print(r.json())

    # 6. Request multiple products to trigger batch processing
    print("Requesting multiple products to trigger batch processing...")
    for _ in range(10):  # Trigger the ORDER_THRESHOLD in order_aggregation_service
        r = requests.post("http://order_service:5003/order", json={"provider_id": provider_id, "product_id": product_id, "quantity": 1})
        print(r.json())

    # 7. Wait for the bulk purchase event to be processed
    print("Waiting for bulk purchase event to be processed...")
    time.sleep(3)  # Give time for the event to be processed

    # 8. Process payment
    print("Processing payment...")
    order_id = 1  # Assuming first order ID
    amount = products[0]["price"] * 2  # Price of the first product times quantity
    r = requests.post("http://payment_service:5004/payment", json={"user": "pedro", "order_id": order_id, "amount": amount})
    try:
        payment_result = r.json()
        print(payment_result)
    except Exception as e:
        print("Error parsing payment response as JSON!")
        print("Status code:", r.status_code)
        print("Response text:", r.text)
        raise e
    
    # The payment service automatically calls the receipt service
    receipt = payment_result.get("receipt")
    print(f"Receipt generated: {receipt}")

    # 9. Wait for notifications to be processed and reports to be generated
    print("Waiting for notifications and reports to be processed...")
    time.sleep(3)  # Give time for notification and report services to process messages

    print("Simulation completed!")
    print("Note: Check the logs of notification_service and report_service to see the message processing")

if __name__ == "__main__":
    simulate_user_flow()
    time.sleep(2)