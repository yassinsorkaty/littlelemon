from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'tables', views.BookingViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'),
    
    # API URLs
    path('api/menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('api/menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='single-menu-item'),
    path('api/message/', views.msg, name='protected-message'),
    path('api/token/', obtain_auth_token, name='api-token-auth'),
    path('api/', include(router.urls)),
]