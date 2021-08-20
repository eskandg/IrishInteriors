from django.urls import path, include
from .models import CaUser, Product, ProductCategory
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CaUser
        fields = '__all__' #
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CaUser(username=validated_data['username'])
        print(validated_data['username'])
        user.set_password(validated_data['password'])
        user.is_admin = False
        user.save()
        return user


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'picture']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'picture']

