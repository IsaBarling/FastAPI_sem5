# Test your FastAPI endpoints
import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the User Management API"}

def test_add_user():
    user_data = {
        "id": "1",
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
    with httpx.Client() as client:
        response = client.post(f"{BASE_URL}/add-user/", json=user_data)
    assert response.status_code == 200
    assert response.json() == user_data

if __name__ == "__main__":
    test_root()
    test_add_user()
    print("All tests passed!")

