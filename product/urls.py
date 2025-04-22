from django.urls import path
from product  import  views


urlpatterns = [
    path('api/v1/categories/', views.CategoriesListCreateAPIView.as_view() ),
    path('api/v1/categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('api/v1/products/', views.ProductListCreateAPIView.as_view()),
    path('api/v1/products/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('api/v1/reviews/', views.ReviewsListAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
]
