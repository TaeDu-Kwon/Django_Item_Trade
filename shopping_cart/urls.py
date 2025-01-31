from django.urls import path

from . import views

app_name = "shopping_cart"

urlpatterns = [
    path('cart/', views.CartViewSet.as_view({'get': 'list'}), name='cart-list'),
    path('cart/<int:pk>/', views.CartViewSet.as_view({'get': 'retrieve'}), name='cart-detail'),

    path('cart-items/', views.CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart-item-list'),
    path('cart-items/<int:user_id>/<int:product_id>/<str:product_type>/', views.CartItemViewSet.as_view({'delete': 'destroy'}), name='cart-item-detail'),
]
