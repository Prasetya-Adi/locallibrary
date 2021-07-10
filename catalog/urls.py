from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Book
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreate.as_view(), name='books-create'),
    path('book/<int:pk>/update/',
         views.BookUpdateView.as_view(), name='book-update'),


    # Author
    path('author/', views.AuthorListView.as_view(), name='author'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/',
         views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/',
         views.AuthorDeleteView.as_view(), name='author-delete'),

    # User
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allborrowed/', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),

    # Staff
    path('book/<uuid:pk>/renew/', views.renew_book_librarian,
         name='renew-book-librarian'),

    # Genre
    path('genre', views.GenreListView.as_view(), name='genre'),
    path('genre/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),
    path('genre/create/', views.GenreCreateView.as_view(), name='genre-create'),
    path('genre/<int:pk>/update/',
         views.GenreUpdateView.as_view(), name='genre-update'),
    path('genre/<int:pk>/delete/',
         views.GenreDeleteView.as_view(), name='genre-delete'),


    # Language
    path('lang', views.LangListView.as_view(), name='lang'),
    path('lang/<int:pk>', views.LangDetailView.as_view(), name='lang-detail'),
    path('lang/create/', views.LangCreateView.as_view(), name='lang-create'),
    path('lang/<int:pk>/update/',
         views.LangUpdateView.as_view(), name='lang-update'),
    path('lang/<int:pk>/delete/',
         views.LangDeleteView.as_view(), name='lang-delete'),

    # BookiInstance
    path('inst', views.InstListView.as_view(), name='inst'),
    path('inst/<uuid:pk>', views.InstDetailView.as_view(), name='inst-detail'),
    path('inst/create/', views.InstCreateView.as_view(), name='inst-create'),
    path('inst/<uuid:pk>/update/',
         views.InstUpdateView.as_view(), name='inst-update'),
    path('inst/<uuid:pk>/delete/',
         views.InstDeleteView.as_view(), name='inst-delete'),

]
