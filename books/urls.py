from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import BookViewSet, GenreListView, GenreRetrieveView, AuthorListView
from accounts.views import CommentViewSet


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')

comments_router = routers.NestedDefaultRouter(router, r'books', lookup='book')
comments_router.register(r'comments', CommentViewSet, basename='book-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
    path('genres/', GenreListView.as_view(), name='genres-list'),
    path('genres/<int:pk>/', GenreRetrieveView.as_view(), name='genres-detail'),
    path('authors/', AuthorListView.as_view(), name='authors-list'),
]