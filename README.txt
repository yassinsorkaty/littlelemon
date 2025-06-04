LITTLE LEMON RESTAURANT - DJANGO CAPSTONE PROJECT
=====================================================

PROJECT OVERVIEW
================
This is a comprehensive Django-based web application for the Little Lemon restaurant, 
featuring both web pages and REST APIs for menu management and table bookings.

FEATURES IMPLEMENTED
===================

Module 1: Project Setup ✅
- Django project created with name 'littlelemon'
- Django app created with name 'restaurant'
- Static files configuration for serving images, CSS, and JavaScript
- Template system configured for rendering HTML pages


Module 2: Project Functionality ✅
- MySQL database connection configured
- Menu model with fields: name, price, menu_item_description
- Booking model with fields: first_name, reservation_date, reservation_slot
- Django REST Framework integration
- Menu API with full CRUD operations
- Table booking API with full CRUD operations
- Model serializers for API data conversion

Module 3: Security and Testing ✅
- User authentication system using Djoser
- Token-based authentication for API security
- User registration, login, and logout functionality
- Protected API endpoints requiring authentication
- Comprehensive unit tests for models
- API endpoint tests using Django REST Framework test client
- Integration tests covering complete user workflows
- Performance tests for bulk operations

API ENDPOINTS WITH FULL TESTING PATHS
=====================================

AUTHENTICATION ENDPOINTS
------------------------
1. User Registration
   URL: POST http://127.0.0.1:8000/auth/users/
   Headers: Content-Type: application/json
   Body: {
       "username": "testuser",
       "password": "testpass123",
       "email": "test@example.com"
   }
   Expected Response: 201 Created with user data

2. User Login (Get Token)
   URL: POST http://127.0.0.1:8000/auth/token/login/
   Headers: Content-Type: application/json
   Body: {
       "username": "testuser",
       "password": "testpass123"
   }
   Expected Response: 200 OK with {"auth_token": "your-token-here"}

3. User Logout
   URL: POST http://127.0.0.1:8000/auth/token/logout/
   Headers: 
       Content-Type: application/json
       Authorization: Token your-token-here
   Body: {}
   Expected Response: 204 No Content

MENU API ENDPOINTS
------------------
Note: All menu endpoints require authentication token in header: Authorization: Token your-token-here

1. List All Menu Items
   URL: GET http://127.0.0.1:8000/restaurant/api/menu-items/
   Headers: Authorization: Token your-token-here
   Expected Response: 200 OK with array of menu items

2. Create New Menu Item
   URL: POST http://127.0.0.1:8000/restaurant/api/menu-items/
   Headers: 
       Content-Type: application/json
       Authorization: Token your-token-here
   Body: {
       "name": "Greek Salad",
       "price": 12,
       "menu_item_description": "Fresh vegetables with feta cheese and olive oil"
   }
   Expected Response: 201 Created with created menu item data

3. Get Specific Menu Item
   URL: GET http://127.0.0.1:8000/restaurant/api/menu-items/{id}/
   Headers: Authorization: Token your-token-here
   Expected Response: 200 OK with menu item data

4. Update Menu Item (Full Update)
   URL: PUT http://127.0.0.1:8000/restaurant/api/menu-items/{id}/
   Headers: 
       Content-Type: application/json
       Authorization: Token your-token-here
   Body: {
       "name": "Updated Greek Salad",
       "price": 15,
       "menu_item_description": "Updated description with premium ingredients"
   }
   Expected Response: 200 OK with updated menu item data

5. Partial Update Menu Item
   URL: PATCH http://127.0.0.1:8000/restaurant/api/menu-items/{id}/
   Headers: 
       Content-Type: application/json
       Authorization: Token your-token-here
   Body: {
       "price": 18
   }
   Expected Response: 200 OK with updated menu item data

6. Delete Menu Item
   URL: DELETE http://127.0.0.1:8000/restaurant/api/menu-items/{id}/
   Headers: Authorization: Token your-token-here
   Expected Response: 204 No Content

BOOKING API ENDPOINTS
---------------------
Note: All booking endpoints require authentication token in header: Authorization: Token your-token-here

1. List All Bookings
   URL: GET http://127.0.0.1:8000/restaurant/api/tables/
   Headers: Authorization: Token your-token-here
   Expected Response: 200 OK with array of bookings

2. Create New Booking
   URL: POST http://127.0.0.1:8000/restaurant/api/tables/
   Headers: 
       Content-Type: application/json
       Authorization: Token your-token-here
   Body: {
       "first_name": "John Doe",
       "reservation_date": "2025-06-15",
       "reservation_slot": 18
   }
   Expected Response: 201 Created with created booking data

3. Get Specific Booking
   URL: GET http://127.0.0.1:8000/restaurant/api/tables/{id}/
   Headers: Authorization: Token your-token-here
   Expected Response: 200 OK with booking data

4. Update Booking (Full Update)
   URL: PUT http://127.0.0.1:8000/restaurant/api/tables/{id}/
   Headers: 
       Content-Type: application/json
       Authorization: Token your-token-here
   Body: {
       "first_name": "Jane Doe",
       "reservation_date": "2025-06-16",
       "reservation_slot": 19
   }
   Expected Response: 200 OK with updated booking data

5. Partial Update Booking
   URL: PATCH http://127.0.0.1:8000/restaurant/api/tables/{id}/
   Headers: 
       Content-Type: application/json
       Authorization: Token your-token-here
   Body: {
       "reservation_slot": 20
   }
   Expected Response: 200 OK with updated booking data

6. Delete Booking
   URL: DELETE http://127.0.0.1:8000/restaurant/api/tables/{id}/
   Headers: Authorization: Token your-token-here
   Expected Response: 204 No Content

WEB PAGE ENDPOINTS
------------------
1. Home Page
   URL: GET http://127.0.0.1:8000/restaurant/
   Expected Response: 200 OK with rendered HTML page

2. About Page
   URL: GET http://127.0.0.1:8000/restaurant/about/
   Expected Response: 200 OK with rendered HTML page

3. Menu Display Page
   URL: GET http://127.0.0.1:8000/restaurant/menu/
   Expected Response: 200 OK with rendered HTML page showing menu items

4. Booking Form Page
   URL: GET http://127.0.0.1:8000/restaurant/book/
   Expected Response: 200 OK with rendered HTML booking form

5. View Reservations Page
   URL: GET http://127.0.0.1:8000/restaurant/reservations/
   Expected Response: 200 OK with rendered HTML page showing reservations

TESTING WORKFLOW WITH INSOMNIA/POSTMAN
======================================

Step 1: Register a New User
---------------------------
1. Send POST request to http://127.0.0.1:8000/auth/users/
2. Use JSON body with username, password, and email
3. Verify 201 Created response

Step 2: Login and Get Authentication Token
------------------------------------------
1. Send POST request to http://127.0.0.1:8000/auth/token/login/
2. Use JSON body with username and password
3. Save the auth_token from response for subsequent requests

Step 3: Test Menu Operations
---------------------------
1. List menus: GET /restaurant/api/menu-items/ (with token header)
2. Create menu: POST /restaurant/api/menu-items/ (with token header and JSON body)
3. Get specific menu: GET /restaurant/api/menu-items/{id}/ (with token header)
4. Update menu: PUT /restaurant/api/menu-items/{id}/ (with token header and JSON body)
5. Delete menu: DELETE /restaurant/api/menu-items/{id}/ (with token header)

Step 4: Test Booking Operations
------------------------------
1. List bookings: GET /restaurant/api/tables/ (with token header)
2. Create booking: POST /restaurant/api/tables/ (with token header and JSON body)
3. Get specific booking: GET /restaurant/api/tables/{id}/ (with token header)
4. Update booking: PUT /restaurant/api/tables/{id}/ (with token header and JSON body)
5. Delete booking: DELETE /restaurant/api/tables/{id}/ (with token header)

Step 5: Test Authentication Protection
-------------------------------------
1. Try accessing any API endpoint without token - should get 401 Unauthorized
2. Try accessing with invalid token - should get 401 Unauthorized
3. Logout: POST /auth/token/logout/ (with token header)
4. Try accessing after logout - should get 401 Unauthorized

MODELS SPECIFICATION
====================

Menu Model:
-----------
class Menu(models.Model):
    name = models.CharField(max_length=200) 
    price = models.IntegerField(null=False) 
    menu_item_description = models.TextField(max_length=1000, default='')

Booking Model:
--------------
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

SECURITY FEATURES
================
- Token-based authentication for all API endpoints
- User registration and login system using Djoser
- Protected views requiring authentication
- CSRF protection for web forms
- Session-based authentication for web interface
- All API endpoints return 401 Unauthorized without valid token

TESTING SUITE
=============

Test Categories:
1. Model Tests (tests/test_models.py)
   - Menu model creation and validation
   - Booking model creation and validation
   - Model string representations
   - Default values testing

2. View Tests (tests/test_views.py)
   - API endpoint testing (GET, POST, PUT, DELETE)
   - Authentication testing
   - Permission testing
   - Web page rendering tests

3. Integration Tests (tests/test_integration.py)
   - Complete user workflow testing
   - CRUD operations testing
   - Performance and bulk operation tests

4. Static Files and Templates (tests/test_static_templates.py)
   - Template rendering tests
   - Static file serving tests
   - URL routing tests

Running Tests:
# Run all tests
pipenv run python manage.py test tests

# Run specific test module
pipenv run python manage.py test tests.test_models

# Run tests with verbose output
pipenv run python manage.py test tests --verbosity=2

# Run custom test runner
pipenv run python run_tests.py

INSTALLATION AND SETUP
======================
Installation Steps:
1. Clone the repository
2. Navigate to project directory
3. Install dependencies:
   pipenv install
4. Configure MySQL database in settings.py
5. Run migrations:
   pipenv run python manage.py migrate
6. Create superuser:
   pipenv run python manage.py createsuperuser
7. Populate sample data:
   pipenv run python manage.py populate_menu
   pipenv run python manage.py populate_bookings
8. Run the server:
   pipenv run python manage.py runserver


