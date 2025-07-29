from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timezone
from .models import Article, Category
from rest_framework.permissions import IsAuthenticated
from .serializers import ArticleSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.permissions import AllowAny
import os
import uuid
from django.utils.deprecation import MiddlewareMixin
from .models import Article
from accounts.models import CustomUser

class ArticleList(APIView):
    permission_classes = [AllowAny]  # Allow public access
    serializer_class = ArticleSerializer
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_request(self):
        queryset = Article.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class ArticleDetail(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            article.views += 1  # Increment the views field
            article.save()  # Save the updated views count
            serializer = ArticleSerializer(article)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ArticleCreateView(APIView):
    def post(self, request):
        try:
            # fetch the logged in users information
            user = request.user
            if not user.is_authenticated:
                return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

            #Prefill author field with the logged-in users info
            author, created = CustomUser.objects.get_or_create(
                user=user,
                defaults={
                    'name': user.username,
                    'bio': 'Superuser bio' if user.is_superuser else '',
                    'image_url': '/default-author-image.jpg'
                }
            )
            # Add the author to the article data
            article_data = request.data.copy()
            

            serializer = ArticleSerializer(data=article_data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ArticleViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/articles/'):
            try:
                article_id = int(request.path.split('/')[-1])
                article = Article.objects.get(pk=article_id)
                article.views += 1
                article.save()
            except (ValueError, Article.DoesNotExist):
                pass

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied.'}, status=403)

        file = request.FILES.get('file')
        if not file:
            return Response({'detail': 'No file provided.'}, status=400)

        try:
            # Use Django settings for portability
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            # Generate a unique filename
            ext = file.name.split('.')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            file_path = os.path.join(upload_dir, filename)

            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            full_url = request.build_absolute_uri(f"{settings.MEDIA_URL}uploads/{filename}")
            return Response({'url': full_url}, status=201)
        except Exception as e:
            return Response({'detail': str(e)}, status=500)


class CategoryList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryArticles(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
            articles = Article.objects.filter(category=category, status='published').order_by('-published_date')
            serializer = ArticleSerializer(articles, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)



class FeaturedArticleView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            featured_article = Article.objects.filter(is_featured=True).order_by('-published_date')[:4]
            if not featured_article:
                return Response({'detail': 'No featured article found.'}, status=status.HTTP_404_NOT_FOUND)

            
            serializer = ArticleSerializer(featured_article, many=True, context={'request': request})
            

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TrendingArticlesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # Fetch articles sorted by views (or another metric)
            trending_articles = Article.objects.order_by('-views')[:10]  # Top 5 articles by views
            serializer = ArticleSerializer(trending_articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class EditorsPicksView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # Fetch articles marked as editor's picks
            editors_picks = Article.objects.filter(is_editors_pick=True)[:5]  # Top 5 editor's picks
            serializer = ArticleSerializer(editors_picks, many=True, context={'request':request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LatestArticlesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # Fetch the latest articles sorted by published_date
            latest_articles = Article.objects.order_by('-published_date')[:20]  # Top 5 latest articles
            serializer = ArticleSerializer(latest_articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RelatedArticlesView(APIView):
    def get(self, request, article_id):
        try:
            # Fetch the current article
            current_article = Article.objects.get(id=article_id)

            # fetch related article
            related_articles = Article.objects.filter(
                category=current_article.category,
                status='published'
            ).exclude(id=article_id)[:12]

            serializer = ArticleSerializer(related_articles, many=True, context={'request': request})
           
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response({'detail': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ArticleSearchView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        if not query:
            return Response([], status=status.HTTP_200_OK)
        articles = Article.objects.filter(title__icontains=query) | Article.objects.filter(excerpt__icontains=query)
        serializer = ArticleSerializer(articles.distinct(), many=True)
        return Response(serializer.data)