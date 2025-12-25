import sys
import os
import json
import random
import string

# Setup path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.main import create_app

def generate_random_email():
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"

def run_tests():
    print("🚀 Starting API Verification...")
    
    # Initialize App
    try:
        app = create_app()
        client = app.test_client()
        print("✅ App Initialized")
    except Exception as e:
        print(f"❌ App Initialization Failed: {e}")
        return

    # Test Data
    test_email = generate_random_email()
    test_password = "Password123!"
    test_user = {
        "email": test_email,
        "username": test_email.split('@')[0],
        "password": test_password,
        "full_name": "Test User"
    }
    
    token = None

    # 1. Test Signup
    print(f"\n1. Testing Signup ({test_email})...")
    try:
        response = client.post('/api/auth/signup', 
                             data=json.dumps(test_user),
                             content_type='application/json')
        
        if response.status_code == 201:
            print("✅ Signup Successful")
            data = json.loads(response.data)
            token = data.get('token')
        else:
            print(f"❌ Signup Failed: {response.status_code} - {response.data}")
            return
    except Exception as e:
        print(f"❌ Signup Exception: {e}")
        return

    # 2. Test Login
    print("\n2. Testing Login...")
    try:
        response = client.post('/api/auth/login',
                             data=json.dumps({
                                 "email": test_email,
                                 "password": test_password
                             }),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("✅ Login Successful")
            if not token:
                token = json.loads(response.data).get('token')
        else:
            print(f"❌ Login Failed: {response.status_code} - {response.data}")
    except Exception as e:
        print(f"❌ Login Exception: {e}")

    # 3. Test Get Citites (Public?)
    # Assuming GET /api/cities might be public or protected. Let's try.
    print("\n3. Testing Get Cities...")
    try:
        response = client.get('/api/cities')
        if response.status_code == 200:
            print(f"✅ Get Cities Successful: {len(json.loads(response.data).get('cities', []))} cities found")
        elif response.status_code == 401:
            print("ℹ️ Get Cities requires auth (Expected)")
            # Try with token if available
            if token:
                response = client.get('/api/cities', headers={'Authorization': f'Bearer {token}'})
                if response.status_code == 200:
                    print(f"✅ Get Cities (Auth) Successful")
                else:
                    print(f"❌ Get Cities (Auth) Failed: {response.status_code}")
        else:
             print(f"❌ Get Cities Failed: {response.status_code} - {response.data}")
    except Exception as e:
        print(f"❌ Get Cities Exception: {e}")

    # 4. Test Token Protected Endpoint (e.g. Navigation History which uses User Tracker)
    print("\n4. Testing Protected Endpoint (Navigation)...")
    if token:
        try:
            # We need user_id for navigation tracking, let's parse from token or response?
            # Actually, the controller extracts user from token.
            # But the endpoint /api/users/navigation/history expects user_id in query param?
            # Let's check UserNavigationController.get_history
            # It expects user_id in args.
            
            # Let's try favorites instead, simpler. FavoriteController.get_all takes current_user.
            
            response = client.get('/api/favorites', headers={'Authorization': f'Bearer {token}'})
            if response.status_code == 200:
                print("✅ Get Favorites Successful")
            else:
                print(f"❌ Get Favorites Failed: {response.status_code} - {response.data}")
        except Exception as e:
            print(f"❌ Protected Endpoint Exception: {e}")
    else:
        print("⚠️ Skipping protected test (No token)")

    # 5. Test Explore City
    print("\n5. Testing Explore City...")
    try:
        response = client.get('/api/cities/explore')
        if response.status_code == 200:
            data = json.loads(response.data)
            city_id = data.get('city_id')
            if city_id:
                print(f"✅ Explore City Successful: Received City ID {city_id}")
            else:
                print(f"❌ Explore City Failed: No city_id in response - {data}")
        else:
            print(f"❌ Explore City Failed: {response.status_code} - {response.data}")
    except Exception as e:
        print(f"❌ Explore City Exception: {e}")

if __name__ == '__main__':
    run_tests()
