from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category,Product
from .serializers import ProductSerializer,CategorySerializer

# Create your views here.
class CategoryListView(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProductListView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ProductByCategoryView(APIView):
    def get(self,request,category_id):
        products =  Product.objects.filter(category_id = category_id)
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)
    
class ProductDetailView(APIView):
    def get(self,request,product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            

