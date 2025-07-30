import json
import random
import string
import requests
from typing import Dict, List, Optional, Any
import os
from datetime import datetime

def create_test_user_data() -> Dict[str, Any]:
    return {
        "name": "Divyaa Selvam",
        "email": "divyaa@example.com",
        "password": "AbcdPass123!",
        "age": 21,
        "role": "user"
    }

def validate_email_format(email: str) -> bool:
    if not isinstance(email, str) or not email:
        return False
    has_at = "@" in email
    has_dot = "." in email
    if has_at and has_dot:
        parts = email.split("@")
        if len(parts) == 2 and parts[0] and parts[1]:
            domain = parts[1]
            return "." in domain and not domain.startswith(".") and not domain.endswith(".")
    return False

def read_test_data_from_json(file_path: str) -> Optional[Dict[str, Any]]:
    try:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return None
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
    return None

class TestUser:
    def __init__(self, name: str, email: str, password: str, age: int = None, role: str = "user"):
        self.name = name
        self.email = email
        self.password = password
        self.age = age
        self.role = role
        self.created_at = datetime.now()

    def validate_user_data(self) -> Dict[str, Any]:
        result = {"is_valid": True, "errors": [], "warnings": []}
        if not self.name:
            result["errors"].append("Name is required")
            result["is_valid"] = False
        if not self.email or not validate_email_format(self.email):
            result["errors"].append("Invalid email format")
            result["is_valid"] = False
        if not self.password:
            result["errors"].append("Password is required")
            result["is_valid"] = False
        elif len(self.password) < 8:
            result["warnings"].append("Password should be at least 8 characters long")
        if self.age is not None and (not isinstance(self.age, int) or self.age < 0 or self.age > 150):
            result["errors"].append("Invalid age value")
            result["is_valid"] = False
        return result

    @classmethod
    def generate_random_test_user(cls) -> 'TestUser':
        name = f"{random.choice(['Prajesh', 'Rodrico'])} {random.choice(['Sadhana', 'Karthick'])}"
        email = f"{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=12))
        age = random.randint(18, 65)
        role = random.choice(["user", "admin", "guest"])
        return cls(name, email, password, age, role)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "age": self.age,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }

    def __str__(self) -> str:
        return f"TestUser(name='{self.name}', email='{self.email}', role='{self.role}')"

class TestDataManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.users: List[TestUser] = []
        self.test_results: List[Dict[str, Any]] = []

    def load_test_users_from_json(self) -> bool:
        data = read_test_data_from_json(self.file_path)
        if not data:
            return False
        self.users.clear()
        for user_data in data.get("users", []):
            user = TestUser(
                name=user_data.get("name", ""),
                email=user_data.get("email", ""),
                password=user_data.get("password", ""),
                age=user_data.get("age"),
                role=user_data.get("role", "user")
            )
            self.users.append(user)
        return True

    def save_test_results_to_file(self, results_file_path: str = None) -> bool:
        if not results_file_path:
            results_file_path = self.file_path.replace('.json', '_results.json')
        try:
            results_data = {
                "timestamp": datetime.now().isoformat(),
                "total_users": len(self.users),
                "test_results": self.test_results,
                "user_validations": [
                    {"user": user.to_dict(), "validation": user.validate_user_data()}
                    for user in self.users
                ]
            }
            with open(results_file_path, 'w', encoding='utf-8') as file:
                json.dump(results_data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False

    def add_test_result(self, test_name: str, result: Any, success: bool) -> None:
        self.test_results.append({
            "test_name": test_name,
            "result": result,
            "success": success,
            "timestamp": datetime.now().isoformat()
        })

    def get_user_count(self) -> int:
        return len(self.users)

    def get_valid_users(self) -> List[TestUser]:
        return [user for user in self.users if user.validate_user_data()["is_valid"]]

    def get_invalid_users(self) -> List[TestUser]:
        return [user for user in self.users if not user.validate_user_data()["is_valid"]]

def safe_web_request(url: str, method: str = "GET", timeout: int = 10, **kwargs) -> Dict[str, Any]:
    result = {
        "success": False, "status_code": None, "data": None,
        "error": None, "url": url, "method": method.upper()
    }
    try:
        if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format")
        response = requests.request(method=method.upper(), url=url, timeout=timeout, **kwargs)
        result["success"] = True
        result["status_code"] = response.status_code
        try:
            result["data"] = response.json()
        except ValueError:
            result["data"] = response.text
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
    return result

def run_simple_test():
    print("Starting Test Framework")
    print("=" * 50)
    
    print("\nTesting Basic Functions:")
    user_data = create_test_user_data()
    print(f"Sample user created: {user_data['name']}")
    
    print("\nTesting Email Validation:")
    test_emails = ["divyaa@example.com", "invalid-email", "test@domain.com"]
    for email in test_emails:
        is_valid = validate_email_format(email)
        status = "Valid" if is_valid else "Invalid"
        print(f"{email} -> {status}")
    
    print("\nTesting User Creation:")
    user = TestUser("Divyaa SK", "divyaa@test.com", "MyPass123!", 21, "admin")
    validation = user.validate_user_data()
    print(f"User created: {user}")
    print(f"Validation: {'Passed' if validation['is_valid'] else 'Failed'}")
    
    print("\nTesting Random User Generation:")
    random_user = TestUser.generate_random_test_user()
    print(f"Random user: {random_user}")
    
    print("\nTesting Data Manager:")
    manager = TestDataManager("test_users.json")
    if manager.load_test_users_from_json():
        print(f"Loaded {manager.get_user_count()} users from JSON")
        print(f"Valid users: {len(manager.get_valid_users())}")
        print(f"Invalid users: {len(manager.get_invalid_users())}")
        if manager.save_test_results_to_file():
            print("Test results saved successfully")
    else:
        print("Failed to load users from JSON")
    
    print("\nTesting Web Request:")
    result = safe_web_request("https://httpbin.org/json", timeout=5)
    status = "Success" if result['success'] else "Failed"
    print(f"Web request: {status}")
    
    print("\nTest execution completed")
    print("=" * 50)

if __name__ == "__main__":
    run_simple_test()
