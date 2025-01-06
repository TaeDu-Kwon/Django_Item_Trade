from django.urls import path
from . import views

urlpatterns = [
    path('game/',views.CreateGameView.as_view()),
    path('create/', views.CreateProductView.as_view(), name='create_product'),
]




