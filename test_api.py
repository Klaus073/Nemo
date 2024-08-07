import requests
import concurrent.futures
import time

def send_request(message, user_id):
    payload = {"message": message, "user_id": user_id}
    print(f"[{time.strftime('%H:%M:%S')}] Sending request for user {user_id}: {payload}")
    start_time = time.time()
    response = requests.post("http://localhost:8000/process", json=payload)
    end_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] Received response for user {user_id}: {response.json()}")
    print(f"[{time.strftime('%H:%M:%S')}] Time taken for user {user_id}: {end_time - start_time:.2f} seconds")

# Sending five requests concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    messages = ["Hello", "How are you?", "Good morning", "Nice to meet you", "Have a great day"]
    user_ids = ["52700585-5642-4366-aded-a9896af705b9", "307c9279-f15f-4da5-b58a-62701a33b8a1", "4ac7a278-41ed-4fff-8db9-c0dadf3fb632", "54040765-0d0f-4b0f-aa62-47c4abe03a71", "f5f5efdb-a3b5-482b-a9d0-be8d4e3cc720"]
    executor.map(send_request, messages, user_ids)


# from database import PostgreSQLConnector

# db = PostgreSQLConnector()
# if db.is_connected():
#     print("connecete")
# else:
#     print("not")