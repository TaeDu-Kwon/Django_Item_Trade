from django.urls import path
from . import views

urlpatterns = [
    path('game/',views.CreateGameView.as_view()),
    path('create/', views.CreateProductView.as_view(), name='create_product'),
    path('get-recently-create-item/',views.ProductViewsets.as_view({
        "get":"get_recently_create_item",
    })),
    path("get-product-info/<str:product_type>/<int:product_id>/",views.ProductViewsets.as_view({
        "get" : "get_product_info"
    }))
]




