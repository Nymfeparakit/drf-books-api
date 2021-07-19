from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, GenreListView, GenreRetrieveView


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
    path('genres/', GenreListView.as_view(), name='genres-list'),
    path('genres/<int:pk>/', GenreRetrieveView.as_view(), name='genres-detail'),
]