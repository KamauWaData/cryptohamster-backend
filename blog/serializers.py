from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Article, Category
from datetime import datetime
from accounts.models import CustomUser




class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'image_url', 'bio']

class ArticleSerializer(serializers.ModelSerializer):
    #published_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    author = AuthorSerializer(read_only=True) 
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        read_only_fields = ['published_date'] 
        fields = '__all__'
    def get_image_url(self, obj):
        request = self.context.get('request', None)
        if request and obj.image_url:
            return request.build_absolute_uri(obj.image_url)
        return None
    
    def create(self, validated_data):
        
        validated_data['author'] = self.context.get('request')
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


