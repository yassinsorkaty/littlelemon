from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from restaurant.models import Menu, Booking
from datetime import date, datetime
import json


class IntegrationTest(APITestCase):
    """Integration tests for the complete workflow"""
    
    def setUp(self):
        """Set up test environment"""
        self.client = APIClient()
        
        # Create test user
        self.user_data = {
            'username': 'integration_user',
            'email': 'integration@test.com',
            'password': 'secure_password123'
        }
        
        # Create some test menu items
        self.menu_items_data = [
            {
                'name': 'Greek Salad',
                'price': 12,
                'menu_item_description': 'Fresh vegetables with feta cheese'
            },
            {
                'name': 'Bruschetta',
                'price': 8,
                'menu_item_description': 'Grilled bread with tomatoes'
            },
            {
                'name': 'Lemon Dessert',
                'price': 6,
                'menu_item_description': 'Traditional lemon dessert'
            }
        ]
    
    def test_complete_user_workflow(self):
        """Test complete user workflow: register, login, browse menu, make booking"""
        
        # Step 1: User Registration
        registration_response = self.client.post('/auth/users/', self.user_data)
        self.assertEqual(registration_response.status_code, status.HTTP_201_CREATED)
        
        # Step 2: User Login to get token
        login_response = self.client.post('/auth/token/login/', {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['auth_token']
        
        # Step 3: Set authentication credentials
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # Step 4: Add menu items (as admin/staff would do)
        for item_data in self.menu_items_data:
            menu_response = self.client.post('/restaurant/api/menu-items/', item_data)
            self.assertEqual(menu_response.status_code, status.HTTP_201_CREATED)
        
        # Step 5: Browse menu items
        menu_list_response = self.client.get('/restaurant/api/menu-items/')
        self.assertEqual(menu_list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(menu_list_response.data), 3)
        
        # Step 6: Make a table booking
        booking_data = {
            'first_name': 'Integration Test User',
            'reservation_date': '2024-12-25',
            'reservation_slot': 18
        }
        booking_response = self.client.post('/restaurant/api/tables/', booking_data)
        self.assertEqual(booking_response.status_code, status.HTTP_201_CREATED)
        
        # Step 7: Verify booking was created
        bookings_response = self.client.get('/restaurant/api/tables/')
        self.assertEqual(bookings_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(bookings_response.data), 1)
        self.assertEqual(bookings_response.data[0]['first_name'], 'Integration Test User')
        
        # Step 8: Update booking
        updated_booking_data = {
            'first_name': 'Updated Test User',
            'reservation_date': '2024-12-25',
            'reservation_slot': 19
        }
        booking_id = bookings_response.data[0]['id']
        update_response = self.client.put(f'/restaurant/api/tables/{booking_id}/', updated_booking_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # Step 9: Verify update
        updated_booking_response = self.client.get(f'/restaurant/api/tables/{booking_id}/')
        self.assertEqual(updated_booking_response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_booking_response.data['first_name'], 'Updated Test User')
        self.assertEqual(updated_booking_response.data['reservation_slot'], 19)
        
        # Step 10: Logout
        logout_response = self.client.post('/auth/token/logout/')
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Step 11: Verify that protected endpoints are no longer accessible
        protected_response = self.client.get('/restaurant/api/menu-items/')
        self.assertEqual(protected_response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_menu_api_crud_operations(self):
        """Test complete CRUD operations for Menu API"""
        
        # Setup authentication
        user = User.objects.create_user(**self.user_data)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        # CREATE - Add new menu item
        create_data = {
            'name': 'Test Dish',
            'price': 15,
            'menu_item_description': 'A test dish for CRUD operations'
        }
        create_response = self.client.post('/restaurant/api/menu-items/', create_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        item_id = create_response.data['id']
        
        # READ - Get the created item
        read_response = self.client.get(f'/restaurant/api/menu-items/{item_id}/')
        self.assertEqual(read_response.status_code, status.HTTP_200_OK)
        self.assertEqual(read_response.data['name'], 'Test Dish')
        
        # UPDATE - Modify the item
        update_data = {
            'name': 'Updated Test Dish',
            'price': 20,
            'menu_item_description': 'An updated test dish'
        }
        update_response = self.client.put(f'/restaurant/api/menu-items/{item_id}/', update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], 'Updated Test Dish')
        self.assertEqual(update_response.data['price'], 20)
        
        # DELETE - Remove the item
        delete_response = self.client.delete(f'/restaurant/api/menu-items/{item_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion
        verify_response = self.client.get(f'/restaurant/api/menu-items/{item_id}/')
        self.assertEqual(verify_response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_booking_api_crud_operations(self):
        """Test complete CRUD operations for Booking API"""
        
        # Setup authentication
        user = User.objects.create_user(**self.user_data)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        # CREATE - Add new booking
        create_data = {
            'first_name': 'John Doe',
            'reservation_date': '2024-12-25',
            'reservation_slot': 18
        }
        create_response = self.client.post('/restaurant/api/tables/', create_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        booking_id = create_response.data['id']
        
        # READ - Get the created booking
        read_response = self.client.get(f'/restaurant/api/tables/{booking_id}/')
        self.assertEqual(read_response.status_code, status.HTTP_200_OK)
        self.assertEqual(read_response.data['first_name'], 'John Doe')
        
        # UPDATE - Modify the booking
        update_data = {
            'first_name': 'Jane Doe',
            'reservation_date': '2024-12-26',
            'reservation_slot': 19
        }
        update_response = self.client.put(f'/restaurant/api/tables/{booking_id}/', update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['first_name'], 'Jane Doe')
        
        # DELETE - Remove the booking
        delete_response = self.client.delete(f'/restaurant/api/tables/{booking_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion
        verify_response = self.client.get(f'/restaurant/api/tables/{booking_id}/')
        self.assertEqual(verify_response.status_code, status.HTTP_404_NOT_FOUND)


class PerformanceTest(TransactionTestCase):
    """Test cases for performance and load handling"""
    
    def setUp(self):
        """Set up test environment"""
        self.user = User.objects.create_user(
            username='perf_user',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_bulk_menu_creation(self):
        """Test creating multiple menu items"""
        menu_items = []
        for i in range(10):
            menu_items.append({
                'name': f'Bulk Item {i}',
                'price': 10 + i,
                'menu_item_description': f'Description for bulk item {i}'
            })
        
        for item in menu_items:
            response = self.client.post('/restaurant/api/menu-items/', item)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify all items were created
        list_response = self.client.get('/restaurant/api/menu-items/')
        self.assertEqual(len(list_response.data), 10)
    
    def test_bulk_booking_creation(self):
        """Test creating multiple bookings"""
        bookings = []
        for i in range(5):
            bookings.append({
                'first_name': f'User {i}',
                'reservation_date': f'2024-12-{25 + i}',
                'reservation_slot': 18 + (i % 3)
            })
        
        for booking in bookings:
            response = self.client.post('/restaurant/api/tables/', booking)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify all bookings were created
        list_response = self.client.get('/restaurant/api/tables/')
        self.assertEqual(len(list_response.data), 5)
