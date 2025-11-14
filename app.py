import requests
from bs4 import BeautifulSoup
import time
import random
import string
from urllib.parse import urljoin

class AutoRegisterTester:
    def __init__(self, base_url, num_iterations=5):
        self.base_url = base_url
        self.num_iterations = num_iterations
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    def generate_random_email(self):
        """Generate random email address"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"test_{random_str}@testmail.com"
    
    def generate_random_name(self):
        """Generate random name"""
        random_str = ''.join(random.choices(string.ascii_letters, k=8))
        return f"User_{random_str}"
    
    def generate_password(self):
        """Generate random password"""
        return ''.join(random.choices(string.ascii_letters + string.digits + '!@#$', k=12))
    
    def get_csrf_token(self):
        """Fetch the register page and extract CSRF token"""
        try:
            response = self.session.get(
                urljoin(self.base_url, '/register'),
                timeout=10
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            
            csrf_token = None
            
         
            csrf_meta = soup.find('meta', {'name': 'csrf-token'})
            if csrf_meta:
                csrf_token = csrf_meta.get('content')
            
          
            if not csrf_token:
                csrf_input = soup.find('input', {'name': '_token'})
                if csrf_input:
                    csrf_token = csrf_input.get('value')
            
           
            if not csrf_token:
                csrf_input = soup.find('input', {'name': 'csrf_token'})
                if csrf_input:
                    csrf_token = csrf_input.get('value')
            
            if csrf_token:
                print(f"✓ CSRF token retrieved: {csrf_token}")
                return csrf_token
            else:
                print("✗ CSRF token not found in page")
                return None
                
        except Exception as e:
            print(f"✗ Error fetching CSRF token: {str(e)}")
            return None
    
    def register(self, name, email, password, csrf_token):
        """Submit registration form with CSRF token"""
        try:
            payload = {
                'name': name,
                'email': email,
                'password': password,
                'password_confirmation': password,
                '_token': csrf_token
            }
            
            response = self.session.post(
                urljoin(self.base_url, '/register'),
                data=payload,
                timeout=10,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                
                if 'logout' in response.text.lower() or 'dashboard' in response.text.lower():
                    print(f"✓ Registration successful: {email}")
                    return True
                else:
                    print(f"✗ Registration failed (status 200 but page indicates failure)")
                    return False
            else:
                print(f"✗ Registration failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Registration error: {str(e)}")
            return False
    
    def logout(self):
        """Logout from the application"""
        try:   
            response = self.session.get(
                urljoin(self.base_url, '/'),
                timeout=10
            )
            
            soup = BeautifulSoup(response.content, 'html.parser')
            csrf_token = None
            
            
            csrf_meta = soup.find('meta', {'name': 'csrf-token'})
            if csrf_meta:
                csrf_token = csrf_meta.get('content')
            
            if not csrf_token:
                csrf_input = soup.find('input', {'name': '_token'})
                if csrf_input:
                    csrf_token = csrf_input.get('value')
            
            if not csrf_token:
                print("⚠ CSRF token not found for logout, attempting without token")
            
            
            payload = {}
            if csrf_token:
                payload['_token'] = csrf_token
            
            response = self.session.post(
                urljoin(self.base_url, '/logout'),
                data=payload,
                timeout=10,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                print("✓ Logout successful")
                return True
            else:
                print(f"✗ Logout failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Logout error: {str(e)}")
            return False
    
    def run_test_cycle(self):
        """Run a single test cycle: get token -> register -> logout"""
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            print("✗ Cannot proceed without CSRF token")
            return False
        
        name = self.generate_random_name()
        email = self.generate_random_email()
        password = self.generate_password()
        
        print(f"\n--- Test Cycle ---")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        
        if self.register(name, email, password, csrf_token):
            time.sleep(2) 
            self.logout()
            return True
        return False
    
    def run_tests(self):
        """Run multiple test cycles"""
        print(f"Starting {self.num_iterations} test cycles...")
        print(f"Target: {self.base_url}\n")
        
        successful = 0
        for i in range(1, self.num_iterations + 1):
            print(f"\n========== Cycle {i}/{self.num_iterations} ==========")
            if self.run_test_cycle():
                successful += 1
            time.sleep(3)  # Delay between cycles
        
        print(f"\n\n========== Test Summary ==========")
        print(f"Total Cycles: {self.num_iterations}")
        print(f"Successful: {successful}")
        print(f"Failed: {self.num_iterations - successful}")


if __name__ == "__main__":
    
    BASE_URL = "url"  
    NUM_ITERATIONS = 10000000000  
    
   
    tester = AutoRegisterTester(BASE_URL, NUM_ITERATIONS)
    tester.run_tests()