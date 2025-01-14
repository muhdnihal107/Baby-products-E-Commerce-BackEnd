from django.urls import path, include
from .views import ProductListView,ProductByCategoryView,CategoryListView,ProductDetailView


urlpatterns = [
    path('list/',ProductListView.as_view(),name='product-list'),
    path('category/',CategoryListView.as_view(),name='category-list'),
    path('category/<int:category_id>',ProductByCategoryView.as_view(),name='product-category'),
    path('<int:product_id>',ProductDetailView.as_view(),name='product-detail'), 
]