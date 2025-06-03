from django.test import TestCase
from restaurant.models import Menu, Booking
from datetime import date


class MenuModelTest(TestCase):
    """Test cases for the Menu model"""
    
    def setUp(self):
        """Set up test data"""
        self.menu_item = Menu.objects.create(
            name="Ice Cream",
            price=8,
            menu_item_description="Delicious vanilla ice cream"
        )
    
    def test_get_item(self):
        """Test the string representation of Menu model"""
        item = Menu.objects.get(name="Ice Cream")
        self.assertEqual(str(item), "Ice Cream : $8")
    
    def test_menu_creation(self):
        """Test that a menu item is created correctly"""
        self.assertEqual(self.menu_item.name, "Ice Cream")
        self.assertEqual(self.menu_item.price, 8)
        self.assertEqual(self.menu_item.menu_item_description, "Delicious vanilla ice cream")
    
    def test_menu_fields(self):
        """Test that menu model has the required fields"""
        self.assertTrue(hasattr(Menu, 'name'))
        self.assertTrue(hasattr(Menu, 'price'))
        self.assertTrue(hasattr(Menu, 'menu_item_description'))


class BookingModelTest(TestCase):
    """Test cases for the Booking model"""
    
    def setUp(self):
        """Set up test data"""
        self.booking = Booking.objects.create(
            first_name="John Doe",
            reservation_date=date(2024, 12, 25),
            reservation_slot=18
        )
    
    def test_booking_creation(self):
        """Test that a booking is created correctly"""
        self.assertEqual(self.booking.first_name, "John Doe")
        self.assertEqual(self.booking.reservation_date, date(2024, 12, 25))
        self.assertEqual(self.booking.reservation_slot, 18)
    
    def test_booking_str(self):
        """Test the string representation of Booking model"""
        expected_str = "John Doe - 2024-12-25"
        self.assertEqual(str(self.booking), expected_str)
    
    def test_booking_fields(self):
        """Test that booking model has the required fields"""
        self.assertTrue(hasattr(Booking, 'first_name'))
        self.assertTrue(hasattr(Booking, 'reservation_date'))
        self.assertTrue(hasattr(Booking, 'reservation_slot'))
    
    def test_default_reservation_slot(self):
        """Test default reservation slot value"""
        booking = Booking.objects.create(
            first_name="Jane Doe",
            reservation_date=date(2024, 12, 26)
        )
        self.assertEqual(booking.reservation_slot, 10)
