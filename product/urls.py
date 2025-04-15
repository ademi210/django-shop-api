from django.urls import path
from product  import  views


urlpatterns = [
    path('api/v1/categories/', views.categories_view ),
    path('api/v1/categories/<int:id>/', views.category_detail_view),
    path('api/v1/products/', views.product_list_view),
    path('api/v1/products/<int:id>/', views.product_detail_view),
    path('api/v1/reviews/', views.reviews_list_view),
    path('api/v1/reviews/<int:id>/', views.review_detail_view ),
]
