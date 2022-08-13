from django.urls import path

from .views import BookListView, BookDetailView, CategoryListView, CategoryDetailView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('post/', CategoryListView.as_view(), name='category_list'),
    path('post/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
]
