from django.urls import path
from .views import ArticleList, ArticleDetail, CategoryList, CategoryDetail, FileUploadView, RelatedArticlesView, ArticleSearchView
from .views import  FeaturedArticleView, TrendingArticlesView, EditorsPicksView, LatestArticlesView, CategoryArticles
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#for development only
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('articles/', ArticleList.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('articles/featured/', FeaturedArticleView.as_view(), name='featured-article'),
    path('articles/trending/', TrendingArticlesView.as_view(), name='trending-articles'),
    path('articles/editors-picks/', EditorsPicksView.as_view(), name='editors-picks'),
    path('articles/latest/', LatestArticlesView.as_view(), name='latest-articles'),
    path('articles/<int:article_id>/related/', RelatedArticlesView.as_view(), name='related-articles'),
    path('categories/', CategoryList.as_view(), name='category-articles'),
    path('categories/<slug:slug>/', CategoryArticles.as_view(), name='category-articles'),
    path('articles/search/', ArticleSearchView.as_view(), name='article-search'),
   
]
#urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)