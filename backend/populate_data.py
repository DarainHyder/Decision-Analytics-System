import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run():
    # 1. Register User
    print("--- 1. Registering User ---")
    user_data = {
        "email": "demo@example.com",
        "name": "Demo User",
        "password": "password123"
    }
    
    # Try registration
    resp = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if resp.status_code == 200:
        print("Registration successful.")
    elif resp.status_code == 400 and "Email already registered" in resp.text:
        print("User already exists. Proceeding to login.")
    else:
        print(f"Registration failed: {resp.status_code} {resp.text}")
        return

    # 2. Login
    print("\n--- 2. Logging In ---")
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if resp.status_code != 200:
        print(f"Login failed: {resp.status_code} {resp.text}")
        return
    
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful. Token acquired.")

    # 3. Create Decision
    print("\n--- 3. Creating Dummy Decision ---")
    decision_payload = {
        "title": "Should I switch to a new job offer?",
        "category": "Career",
        "description": "I received an offer from TechCorp with a 20% salary increase but less remote work flexibility. Current job is stable but stagnant.",
        "confidence_score": 65,
        "expected_outcome": "Better career growth and financial stability, successfully managing the commute.",
        "decision_date": "2023-10-27T10:00:00",
        "options": [
            {
                "option_name": "Accept Offer",
                "reasoning": "Higher pay, new challenges, better brand name."
            },
            {
                "option_name": "Stay at Current Job",
                "reasoning": "Comfortable, fully remote, good work-life balance."
            },
            {
                "option_name": "Negotiate Current Job",
                "reasoning": "Try to get a raise to match the offer while keeping remote work."
            }
        ],
        "assumptions": [
            {
                "assumption_text": "The commute to TechCorp won't be exhausting (3 days/week).",
                "status": "pending"
            },
            {
                "assumption_text": "My current boss won't match the salary offer.",
                "status": "pending"
            }
        ]
    }

    resp = requests.post(f"{BASE_URL}/decisions/", json=decision_payload, headers=headers)
    if resp.status_code == 200:
        decision = resp.json()
        print(f"Decision created successfully! ID: {decision['id']}")
        print(f"Title: {decision['title']}")
        print(f"Options: {len(decision['options'])}")
    else:
        print(f"Failed to create decision: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    run()
