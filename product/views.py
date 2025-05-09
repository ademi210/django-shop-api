from unicodedata import category
from . import models, serializers
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import  Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductValidateSerializer, \
    CategoryValidateSerializer, ReviewValidateSerializer



class ProductListCreateAPIView(ListCreateAPIView):
    queryset = (Product.objects.select_related('category')
                .prefetch_related('reviews').all())
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        validator = ProductValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)

        title = validator.validated_data.get('title')
        description = validator.validated_data.get('description')
        price = validator.validated_data.get('price')

        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
            )
            product.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ProductSerializer(product).data)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        product_detail = self.get_object()
        validator = serializers.ProductValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        product_detail.title = validator.validated_data.get('title')
        product_detail.description = validator.validated_data.get('description')
        product_detail.price = validator.validated_data.get('price')
        product_detail.save()
        return Response(serializers.ProductSerializer(product_detail).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoriesListCreateAPIView(ListCreateAPIView):
    queryset = (Category.objects.all())
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        validator = serializers.CategoryValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        name = validator.validated_data.get('name')

        with transaction.atomic():
            category = Category.objects.create(
                name=name
            )
        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(category).data)

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        category_detail = self.get_object()
        validator = serializers.CategoryValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        category.name = validator.validated_data.get('name')
        category_detail.save()
        return Response(serializers.CategorySerializer(category_detail).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewsListAPIView(ListCreateAPIView):
    queryset = (Review.objects.all())
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text')
        product = serializer.validated_data.get('product')
        stars = serializer.validated_data.get('stars')
        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                product=product,
                stars=stars
            )
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        review_detail = self.get_object()
        validator = serializers.ReviewValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        review_detail.text = validator.validated_data.get('text')
        review_detail.product = validator.validated_data.get('product')
        review_detail.stars = validator.validated_data.get('stars')
        review_detail.save()
        return Response(serializers.ReviewSerializer(review_detail).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# @api_view(http_method_names=['GET','POST'])
# def reviews_list_view(request):
#     if request.method == 'GET':
#         review = (Review.objects.select_related('product'))
#         data = ReviewSerializer(instance=review, many=True).data
#         return Response(data=data,
#                             status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#
#         text = serializer.validated_data.get('text')
#         product = serializer.validated_data.get('product')
#         stars = serializer.validated_data.get('stars')
#
#         with transaction.atomic():
#             review = Review.objects.create(
#                 text=text,
#                 product=product,
#                 stars=stars
#             )
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ReviewSerializer(review).data)
#
#
# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def review_detail_view(request, id):
#     try:
#         review = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND,
#                         data={'errors': 'Review does not exist!'})
#
#     if request.method == 'GET':
#         data = ReviewSerializer(review).data
#         return Response(data=data)
#
#     elif request.method == 'PUT':
#         serializer = ReviewValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         product_id = serializer.validated_data.get('product')
#
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND,
#                             data={'error': 'Product not found'})
#
#         review.text = serializer.validated_data.get('text')
#         review.product = product
#         review.stars = serializer.validated_data.get('stars')
#         review.save()
#
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ReviewSerializer(review).data)
#
#     else:
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class CategoryListView(generics.ListAPIView):
#     queryset = Category.objects.annotate(product_count=Count('products'))
#     serializer_class = CategorySerializer


# class CategoryDetailView(generics.RetrieveAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductDetailView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
#
# class ProductReviewsView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
#
# class ReviewListView(generics.ListAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#
# class ReviewDetailView(generics.RetrieveAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer




# @api_view(http_method_names=['GET','POST'])
# def product_list_view(request):
#     if request.method == 'GET':
#         products = (Product.objects.select_related('category')
#                      .prefetch_related('reviews').all())
#         data = ProductSerializer(instance=products, many=True).data
#         return Response(data=data,
#                             status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#
#         title = serializer.validated_data.get('title')
#         description = serializer.validated_data.get('description')
#         price = serializer.validated_data.get('price')
#
#         with transaction.atomic():
#             product = Product.objects.create(
#                 title=title,
#                 description=description,
#                 price=price
#             )
#
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ProductSerializer(product).data)


# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def product_detail_view(request, id):
#     try:
#         product = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND,
#                         data={'errors': 'Product does not exist!'})
#     if request.method == 'GET':
#         data = ProductSerializer(product).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = ProductValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         product.title = serializer.validated_data.get('title')
#         product.description = serializer.validated_data.get('description')
#         product.price = serializer.validated_data.get('price')
#         product.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ProductSerializer(product).data)
#     else:
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# @api_view(http_method_names=['GET','POST'])
# def categories_view(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         data = CategorySerializer(instance=categories, many=True).data
#         return Response(data=data,
#                             status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = CategoryValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
#
#         name = serializer.validated_data.get('name')
#
#         with transaction.atomic():
#             category = Category.objects.create(
#                 name=name
#             )
#
#
#         return Response(status=status.HTTP_201_CREATED,
#                         data=CategorySerializer(category)).data

#
# @api_view(http_method_names=['GET','PUT', 'DELETE'])
# def category_detail_view(request, id):
#     try:
#         category = Category.objects.get(id=id)
#     except Category.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND,
#                         data={'errors': 'Category does not exist!'})
#     if request.method == 'GET':
#         data = CategorySerializer(category).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = CategoryValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         category.name = serializer.validated_data.get('name')
#         category.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=CategorySerializer(category).data)
#     else:
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#