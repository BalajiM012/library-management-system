import requests

session = requests.Session()

# Updated with correct username and password
login_data = {
    "username": "admin",
    "password": "adminpassword"
}

login_url = "http://127.0.0.1:5000/api/student_login/login"
history_url = "http://127.0.0.1:5000/history"
borrow_api_url = "http://127.0.0.1:5000/api/history/borrow"
fees_api_url = "http://127.0.0.1:5000/api/history/fees"

# Login
response = session.post(login_url, json=login_data)
print("Login response:", response.json())

if response.status_code == 200:
    # Access history page
    history_page = session.get(history_url)
    print("History page status code:", history_page.status_code)

    # Access borrow history API
    borrow_response = session.get(borrow_api_url)
    print("Borrow history API response:", borrow_response.json())

    # Access fees API
    fees_response = session.get(fees_api_url)
    print("Fees API response:", fees_response.json())
else:
    print("Login failed, cannot test history feature.")
