from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ('id', 'name', 'product_count')


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
        fields = ('id', 'title', 'reviews', 'average_rating')






