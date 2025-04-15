from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'product_count')
    def get_product_count(self, obj):
        return obj.products.count()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'stars', 'text')

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, product):
        reviews = product.reviews.all()
        if reviews.exists():
            total_stars = sum([review.stars for review in reviews])
            return total_stars / reviews.count()
        return 0

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'reviews', 'average_rating')

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    description = serializers.CharField()
    price = serializers.FloatField(default=0)

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    product = serializers.IntegerField()
    stars = serializers.IntegerField(min_value=1, max_value=5)
