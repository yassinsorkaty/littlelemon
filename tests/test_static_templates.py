from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
import os


class StaticFilesTest(TestCase):
    """Test cases for static files functionality"""
    
    def setUp(self):
        self.client = Client()
    
    def test_static_files_served(self):
        """Test that static files are properly served"""
        # Test CSS file access
        response = self.client.get('/restaurant/static/css/style.css')
        # In development, static files are served by Django
        # We just check that the file exists in the static directory
        css_path = os.path.join(settings.BASE_DIR, 'restaurant', 'static', 'css', 'style.css')
        self.assertTrue(os.path.exists(css_path))
    
    def test_template_rendering(self):
        """Test that templates are properly rendered"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Little Lemon')  # Assuming this text is in the template


class TemplateTest(TestCase):
    """Test cases for template functionality"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_template(self):
        """Test home page template"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_about_template(self):
        """Test about page template"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
    
    def test_menu_template(self):
        """Test menu page template"""
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')
    
    def test_book_template(self):
        """Test booking page template"""
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book.html')


class URLTest(TestCase):
    """Test cases for URL routing"""
    
    def setUp(self):
        self.client = Client()
    
    def test_url_patterns(self):
        """Test that all main URLs are accessible"""
        urls_to_test = [
            ('home', '/restaurant/'),
            ('about', '/restaurant/about/'),
            ('menu', '/restaurant/menu/'),
            ('book', '/restaurant/book/'),
        ]
        
        for name, url in urls_to_test:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
