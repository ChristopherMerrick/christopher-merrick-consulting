#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Christopher Merrick Database Consulting Website
Tests all API endpoints, authentication, database operations, and data initialization
"""

import requests
import json
import os
from datetime import datetime
import sys

# Load environment variables
def load_env_vars():
    """Load environment variables from frontend .env file"""
    env_path = "/app/frontend/.env"
    env_vars = {}
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value.strip('"')
    except FileNotFoundError:
        print(f"Warning: {env_path} not found")
    return env_vars

# Get backend URL
env_vars = load_env_vars()
BACKEND_URL = env_vars.get('REACT_APP_BACKEND_URL', 'http://localhost:8001') + '/api'

print(f"Testing backend at: {BACKEND_URL}")

class BackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.auth_token = None
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        
    def log_result(self, test_name, success, message="", error_details=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        if error_details:
            print(f"   Error: {error_details}")
            self.test_results['errors'].append(f"{test_name}: {error_details}")
        
        if success:
            self.test_results['passed'] += 1
        else:
            self.test_results['failed'] += 1
        print()

    def test_database_connection(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Database Connection", True, f"API responded: {data.get('message', 'OK')}")
                return True
            else:
                self.log_result("Database Connection", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Database Connection", False, "Connection failed", str(e))
            return False

    def test_admin_authentication(self):
        """Test admin login and JWT token generation"""
        try:
            # Test admin login
            login_data = {
                "email": "admin@christophermerrick.co.uk",
                "password": "admin123"
            }
            
            response = requests.post(f"{self.base_url}/auth/login", json=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and 'token_type' in data:
                    self.auth_token = data['access_token']
                    self.log_result("Admin Authentication - Login", True, "JWT token generated successfully")
                    
                    # Test token validation with /auth/me
                    headers = {"Authorization": f"Bearer {self.auth_token}"}
                    me_response = requests.get(f"{self.base_url}/auth/me", headers=headers, timeout=10)
                    
                    if me_response.status_code == 200:
                        user_data = me_response.json()
                        if user_data.get('email') == 'admin@christophermerrick.co.uk':
                            self.log_result("Admin Authentication - Token Validation", True, f"User: {user_data.get('name', 'Unknown')}")
                            return True
                        else:
                            self.log_result("Admin Authentication - Token Validation", False, "Invalid user data returned")
                    else:
                        self.log_result("Admin Authentication - Token Validation", False, f"HTTP {me_response.status_code}", me_response.text)
                else:
                    self.log_result("Admin Authentication - Login", False, "Missing token in response", str(data))
            else:
                self.log_result("Admin Authentication - Login", False, f"HTTP {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("Admin Authentication", False, "Authentication failed", str(e))
        
        return False

    def test_public_endpoints(self):
        """Test all public API endpoints"""
        endpoints = [
            ("/services", "Services API"),
            ("/testimonials", "Testimonials API"),
            ("/blog", "Blog API")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        self.log_result(f"Public API - {name}", True, f"Returned {len(data)} items")
                    else:
                        self.log_result(f"Public API - {name}", False, "Expected list response", str(data))
                else:
                    self.log_result(f"Public API - {name}", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result(f"Public API - {name}", False, "Request failed", str(e))

    def test_contact_form(self):
        """Test contact form submission"""
        try:
            contact_data = {
                "name": "James Wilson",
                "email": "james.wilson@techcorp.co.uk",
                "phone": "07123456789",
                "company": "TechCorp Solutions Ltd",
                "consultationType": "Database Consulting",
                "message": "We need help optimizing our Access database for better performance. Our current system is slow with large datasets."
            }
            
            response = requests.post(f"{self.base_url}/contact", json=contact_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'id' in data:
                    self.log_result("Contact Form Submission", True, f"Contact saved with ID: {data['id']}")
                    return data['id']
                else:
                    self.log_result("Contact Form Submission", False, "Invalid response format", str(data))
            else:
                self.log_result("Contact Form Submission", False, f"HTTP {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("Contact Form Submission", False, "Submission failed", str(e))
        
        return None

    def test_newsletter_subscription(self):
        """Test newsletter subscription"""
        try:
            subscription_data = {
                "email": "newsletter.subscriber@example.co.uk"
            }
            
            response = requests.post(f"{self.base_url}/newsletter", json=subscription_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result("Newsletter Subscription", True, data.get('message', 'Subscribed successfully'))
                else:
                    self.log_result("Newsletter Subscription", False, "Subscription failed", str(data))
            else:
                self.log_result("Newsletter Subscription", False, f"HTTP {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("Newsletter Subscription", False, "Subscription failed", str(e))

    def test_protected_routes_without_auth(self):
        """Test that protected routes require authentication"""
        protected_endpoints = [
            "/admin/blog",
            "/admin/testimonials", 
            "/admin/contacts",
            "/admin/services",
            "/admin/analytics"
        ]
        
        for endpoint in protected_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code == 401:
                    self.log_result(f"Protected Route - {endpoint}", True, "Correctly requires authentication")
                else:
                    self.log_result(f"Protected Route - {endpoint}", False, f"Should return 401, got {response.status_code}")
            except Exception as e:
                self.log_result(f"Protected Route - {endpoint}", False, "Request failed", str(e))

    def test_admin_endpoints(self):
        """Test admin endpoints with authentication"""
        if not self.auth_token:
            self.log_result("Admin Endpoints", False, "No auth token available", "Authentication must pass first")
            return
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test GET endpoints
        get_endpoints = [
            ("/admin/blog", "Admin Blog Management"),
            ("/admin/testimonials", "Admin Testimonials Management"),
            ("/admin/contacts", "Admin Contacts Management"),
            ("/admin/services", "Admin Services Management"),
            ("/admin/analytics", "Admin Analytics")
        ]
        
        for endpoint, name in get_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log_result(f"{name} - GET", True, f"Retrieved data successfully")
                else:
                    self.log_result(f"{name} - GET", False, f"HTTP {response.status_code}", response.text)
            except Exception as e:
                self.log_result(f"{name} - GET", False, "Request failed", str(e))

    def test_blog_crud_operations(self):
        """Test blog post CRUD operations"""
        if not self.auth_token:
            self.log_result("Blog CRUD Operations", False, "No auth token available")
            return
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        created_post_id = None
        
        # CREATE - Test blog post creation
        try:
            blog_data = {
                "title": "Database Performance Optimization Tips",
                "slug": "database-performance-optimization-tips",
                "excerpt": "Learn essential techniques to improve your database performance and reduce query times.",
                "content": "# Database Performance Optimization Tips\n\nDatabase performance is crucial for business applications...",
                "category": "Performance",
                "readTime": "8 min read",
                "published": True,
                "seoTitle": "Database Performance Optimization Tips | Christopher Merrick",
                "seoDescription": "Expert tips for optimizing database performance and improving query response times."
            }
            
            response = requests.post(f"{self.base_url}/admin/blog", json=blog_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data or '_id' in data:
                    created_post_id = data.get('id') or data.get('_id')
                    self.log_result("Blog CRUD - CREATE", True, f"Blog post created with ID: {created_post_id}")
                else:
                    self.log_result("Blog CRUD - CREATE", False, "No ID in response", str(data))
            else:
                self.log_result("Blog CRUD - CREATE", False, f"HTTP {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("Blog CRUD - CREATE", False, "Creation failed", str(e))
        
        # UPDATE - Test blog post update
        if created_post_id:
            try:
                update_data = {
                    "title": "Advanced Database Performance Optimization Tips",
                    "slug": "advanced-database-performance-optimization-tips",
                    "excerpt": "Advanced techniques for database performance optimization.",
                    "content": "# Advanced Database Performance Optimization Tips\n\nAdvanced database performance techniques...",
                    "category": "Advanced Performance",
                    "readTime": "10 min read",
                    "published": True
                }
                
                response = requests.put(f"{self.base_url}/admin/blog/{created_post_id}", json=update_data, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    self.log_result("Blog CRUD - UPDATE", True, "Blog post updated successfully")
                else:
                    self.log_result("Blog CRUD - UPDATE", False, f"HTTP {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_result("Blog CRUD - UPDATE", False, "Update failed", str(e))
        
        # DELETE - Test blog post deletion
        if created_post_id:
            try:
                response = requests.delete(f"{self.base_url}/admin/blog/{created_post_id}", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_result("Blog CRUD - DELETE", True, "Blog post deleted successfully")
                    else:
                        self.log_result("Blog CRUD - DELETE", False, "Delete operation failed", str(data))
                else:
                    self.log_result("Blog CRUD - DELETE", False, f"HTTP {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_result("Blog CRUD - DELETE", False, "Deletion failed", str(e))

    def test_testimonial_crud_operations(self):
        """Test testimonial CRUD operations"""
        if not self.auth_token:
            self.log_result("Testimonial CRUD Operations", False, "No auth token available")
            return
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        created_testimonial_id = None
        
        # CREATE - Test testimonial creation
        try:
            testimonial_data = {
                "name": "Michael Roberts",
                "company": "Roberts Engineering Ltd",
                "location": "Liverpool",
                "text": "Christopher's database solution transformed our project management process. The custom reporting features have given us insights we never had before.",
                "rating": 5,
                "published": True
            }
            
            response = requests.post(f"{self.base_url}/admin/testimonials", json=testimonial_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data or '_id' in data:
                    created_testimonial_id = data.get('id') or data.get('_id')
                    self.log_result("Testimonial CRUD - CREATE", True, f"Testimonial created with ID: {created_testimonial_id}")
                else:
                    self.log_result("Testimonial CRUD - CREATE", False, "No ID in response", str(data))
            else:
                self.log_result("Testimonial CRUD - CREATE", False, f"HTTP {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("Testimonial CRUD - CREATE", False, "Creation failed", str(e))
        
        # UPDATE - Test testimonial update
        if created_testimonial_id:
            try:
                update_data = {
                    "name": "Michael Roberts",
                    "company": "Roberts Engineering Solutions Ltd",
                    "location": "Liverpool",
                    "text": "Christopher's database solution completely transformed our project management process. The custom reporting and analytics features have given us business insights we never had before.",
                    "rating": 5,
                    "published": True
                }
                
                response = requests.put(f"{self.base_url}/admin/testimonials/{created_testimonial_id}", json=update_data, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    self.log_result("Testimonial CRUD - UPDATE", True, "Testimonial updated successfully")
                else:
                    self.log_result("Testimonial CRUD - UPDATE", False, f"HTTP {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_result("Testimonial CRUD - UPDATE", False, "Update failed", str(e))
        
        # DELETE - Test testimonial deletion
        if created_testimonial_id:
            try:
                response = requests.delete(f"{self.base_url}/admin/testimonials/{created_testimonial_id}", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_result("Testimonial CRUD - DELETE", True, "Testimonial deleted successfully")
                    else:
                        self.log_result("Testimonial CRUD - DELETE", False, "Delete operation failed", str(data))
                else:
                    self.log_result("Testimonial CRUD - DELETE", False, f"HTTP {response.status_code}", response.text)
                    
            except Exception as e:
                self.log_result("Testimonial CRUD - DELETE", False, "Deletion failed", str(e))

    def test_data_initialization(self):
        """Test that default data was properly initialized"""
        try:
            # Check if default services exist
            response = requests.get(f"{self.base_url}/services", timeout=10)
            if response.status_code == 200:
                services = response.json()
                if len(services) >= 3:  # Should have at least 3 default services
                    service_titles = [s.get('title', '') for s in services]
                    expected_services = ['Custom Access Databases', 'Data Analysis & Insights', 'Database Consulting']
                    found_services = [title for title in expected_services if any(title in st for st in service_titles)]
                    
                    if len(found_services) >= 2:
                        self.log_result("Data Initialization - Services", True, f"Found {len(services)} services including default ones")
                    else:
                        self.log_result("Data Initialization - Services", False, f"Missing expected default services", f"Found: {service_titles}")
                else:
                    self.log_result("Data Initialization - Services", False, f"Expected at least 3 services, found {len(services)}")
            else:
                self.log_result("Data Initialization - Services", False, f"HTTP {response.status_code}", response.text)
                
            # Check if default testimonials exist
            response = requests.get(f"{self.base_url}/testimonials", timeout=10)
            if response.status_code == 200:
                testimonials = response.json()
                if len(testimonials) >= 3:  # Should have at least 3 default testimonials
                    self.log_result("Data Initialization - Testimonials", True, f"Found {len(testimonials)} testimonials")
                else:
                    self.log_result("Data Initialization - Testimonials", False, f"Expected at least 3 testimonials, found {len(testimonials)}")
            else:
                self.log_result("Data Initialization - Testimonials", False, f"HTTP {response.status_code}", response.text)
                
            # Check if default blog posts exist
            response = requests.get(f"{self.base_url}/blog", timeout=10)
            if response.status_code == 200:
                blog_posts = response.json()
                if len(blog_posts) >= 2:  # Should have at least 2 default blog posts
                    self.log_result("Data Initialization - Blog Posts", True, f"Found {len(blog_posts)} blog posts")
                else:
                    self.log_result("Data Initialization - Blog Posts", False, f"Expected at least 2 blog posts, found {len(blog_posts)}")
            else:
                self.log_result("Data Initialization - Blog Posts", False, f"HTTP {response.status_code}", response.text)
                
        except Exception as e:
            self.log_result("Data Initialization", False, "Initialization check failed", str(e))

    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 80)
        print("CHRISTOPHER MERRICK DATABASE CONSULTING - BACKEND TESTING")
        print("=" * 80)
        print()
        
        # Test basic connectivity first
        if not self.test_database_connection():
            print("❌ CRITICAL: Cannot connect to backend API. Stopping tests.")
            return self.test_results
        
        # Test authentication
        self.test_admin_authentication()
        
        # Test public endpoints
        self.test_public_endpoints()
        
        # Test contact form
        self.test_contact_form()
        
        # Test newsletter subscription
        self.test_newsletter_subscription()
        
        # Test protected routes without auth
        self.test_protected_routes_without_auth()
        
        # Test admin endpoints
        self.test_admin_endpoints()
        
        # Test CRUD operations
        self.test_blog_crud_operations()
        self.test_testimonial_crud_operations()
        
        # Test data initialization
        self.test_data_initialization()
        
        # Print summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"✅ PASSED: {self.test_results['passed']}")
        print(f"❌ FAILED: {self.test_results['failed']}")
        print(f"📊 TOTAL:  {self.test_results['passed'] + self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\n🔍 ERRORS FOUND:")
            for error in self.test_results['errors']:
                print(f"   • {error}")
        
        print("=" * 80)
        
        return self.test_results

if __name__ == "__main__":
    tester = BackendTester()
    results = tester.run_all_tests()
    
    # Exit with error code if tests failed
    if results['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)