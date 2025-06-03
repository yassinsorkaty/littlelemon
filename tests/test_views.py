from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from restaurant.models import Menu, Booking
from restaurant.serializers import MenuSerializer, BookingSerializer
from datetime import date
import json


class MenuViewTest(TestCase):
    """Test cases for Menu views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.menu_item1 = Menu.objects.create(
            name="Greek Salad",
            price=12,
            menu_item_description="Fresh Greek salad with feta cheese"
        )
        self.menu_item2 = Menu.objects.create(
            name="Bruschetta",
            price=8,
            menu_item_description="Grilled bread with tomatoes"
        )
    
    def test_get_menu_page(self):
        """Test GET request to menu page"""
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Greek Salad')
        self.assertContains(response, 'Bruschetta')
    
    def test_get_menu_item_page(self):
        """Test GET request to specific menu item page"""
        response = self.client.get(reverse('menu_item', kwargs={'pk': self.menu_item1.id}))
        self.assertEqual(response.status_code, 200)


class MenuAPITest(APITestCase):
    """Test cases for Menu API endpoints"""
    
    def setUp(self):
        """Set up test data and authentication"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.menu_item = Menu.objects.create(
            name="Test Dish",
            price=15,
            menu_item_description="A test dish for API testing"
        )
    
    def test_get_all_menu_items(self):
        """Test GET request to retrieve all menu items"""
        response = self.client.get('/restaurant/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        menu_items = Menu.objects.all()
        serializer = MenuSerializer(menu_items, many=True)
        self.assertEqual(response.data, serializer.data)
    
    def test_get_menu_item_by_id(self):
        """Test GET request to retrieve a specific menu item"""
        response = self.client.get(f'/restaurant/api/menu-items/{self.menu_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        serializer = MenuSerializer(self.menu_item)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_menu_item(self):
        """Test POST request to create a new menu item"""
        data = {
            'name': 'New Dish',
            'price': 20,
            'menu_item_description': 'A newly created dish'
        }
        response = self.client.post('/restaurant/api/menu-items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(Menu.objects.latest('id').name, 'New Dish')
    
    def test_update_menu_item(self):
        """Test PUT request to update a menu item"""
        data = {
            'name': 'Updated Dish',
            'price': 25,
            'menu_item_description': 'An updated dish description'
        }
        response = self.client.put(f'/restaurant/api/menu-items/{self.menu_item.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, 'Updated Dish')
        self.assertEqual(self.menu_item.price, 25)
    
    def test_delete_menu_item(self):
        """Test DELETE request to remove a menu item"""
        response = self.client.delete(f'/restaurant/api/menu-items/{self.menu_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 0)
    
    def test_unauthorized_access(self):
        """Test that unauthorized requests are rejected"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/restaurant/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookingAPITest(APITestCase):
    """Test cases for Booking API endpoints"""
    
    def setUp(self):
        """Set up test data and authentication"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.booking = Booking.objects.create(
            first_name="John Smith",
            reservation_date=date(2024, 12, 25),
            reservation_slot=19
        )
    
    def test_get_all_bookings(self):
        """Test GET request to retrieve all bookings"""
        response = self.client.get('/restaurant/api/tables/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_booking(self):
        """Test POST request to create a new booking"""
        data = {
            'first_name': 'Jane Doe',
            'reservation_date': '2024-12-26',
            'reservation_slot': 20
        }
        response = self.client.post('/restaurant/api/tables/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
    
    def test_update_booking(self):
        """Test PUT request to update a booking"""
        data = {
            'first_name': 'John Updated',
            'reservation_date': '2024-12-25',
            'reservation_slot': 20
        }
        response = self.client.put(f'/restaurant/api/tables/{self.booking.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.first_name, 'John Updated')
        self.assertEqual(self.booking.reservation_slot, 20)
    
    def test_delete_booking(self):
        """Test DELETE request to remove a booking"""
        response = self.client.delete(f'/restaurant/api/tables/{self.booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)


class BookingViewTest(TestCase):
    """Test cases for booking views and functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.booking_data = {
            'first_name': 'Test User',
            'reservation_date': '2024-12-25',
            'reservation_slot': 18
        }
    
    def test_bookings_post_request(self):
        """Test POST request to bookings endpoint"""
        response = self.client.post(
            '/restaurant/bookings',
            data=json.dumps(self.booking_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_duplicate_booking_prevention(self):
        """Test that duplicate bookings are prevented"""
        # Create first booking
        Booking.objects.create(
            first_name='Existing User',
            reservation_date=date(2024, 12, 25),
            reservation_slot=18
        )
        
        # Try to create duplicate booking
        response = self.client.post(
            '/restaurant/bookings',
            data=json.dumps(self.booking_data),
            content_type='application/json'
        )
        
        # Should return error
        self.assertContains(response, 'error')
    
    def test_bookings_get_request(self):
        """Test GET request to bookings endpoint"""
        # Create a booking
        Booking.objects.create(
            first_name='Test User',
            reservation_date=date.today(),
            reservation_slot=18
        )
        
        response = self.client.get('/restaurant/bookings')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')


class AuthenticationTest(APITestCase):
    """Test cases for authentication functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_user_registration(self):
        """Test user registration through djoser"""
        response = self.client.post('/auth/users/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_token_authentication(self):
        """Test token-based authentication"""
        # Create user
        user = User.objects.create_user(**self.user_data)
        
        # Get token
        response = self.client.post('/auth/token/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)
        
        # Use token to access protected endpoint
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        protected_response = self.client.get('/restaurant/api/message/')
        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)
        self.assertEqual(protected_response.data['message'], "This view is protected")
    
    def test_token_logout(self):
        """Test token logout functionality"""
        # Create user and get token
        user = User.objects.create_user(**self.user_data)
        login_response = self.client.post('/auth/token/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        token = login_response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # Logout
        logout_response = self.client.post('/auth/token/logout/')
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Try to access protected endpoint after logout
        protected_response = self.client.get('/restaurant/api/message/')
        self.assertEqual(protected_response.status_code, status.HTTP_401_UNAUTHORIZED)
