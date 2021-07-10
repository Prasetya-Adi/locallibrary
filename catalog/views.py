import datetime
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from catalog.forms import RenewBookForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.
from .models import Book, Author, BookInstance, Genre, Language
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required

# Index


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # The 'all()' is implied by default.
    num_genre = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'num_genre': num_genre,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Book


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class BookCreate(CreateView):
    model = Book
    fields = '__all__'


class BookUpdateView(UpdateView):
    model = Book
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'

# Author


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorCreateView(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    template_name = 'catalog/author_form.html'


class AuthorUpdateView(UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('author')

# User


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

# staff


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

# Genre


class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 10


class GenreDetailView(generic.DetailView):
    model = Genre


class GenreCreateView(CreateView):
    model = Genre
    fields = '__all__'
    template_name = 'catalog/genre_form.html'
    success_url = reverse_lazy('genre')


class GenreUpdateView(UpdateView):
    model = Genre
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class GenreDeleteView(DeleteView):
    model = Language
    success_url = reverse_lazy('genre')


# Language

class LangListView(generic.ListView):
    model = Language


class LangDetailView(generic.DetailView):
    model = Language


class LangCreateView(CreateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('lang')
    initial = {'name': ''}


class LangUpdateView(UpdateView):
    model = Language
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class LangDeleteView(DeleteView):
    model = Language
    success_url = reverse_lazy('lang')

# Instance


class InstListView(generic.ListView):
    model = BookInstance
    paginate_by = 20
    ordering = ['-due_back']


class InstDetailView(generic.DetailView):
    model = BookInstance


class InstCreateView(CreateView):
    model = BookInstance
    fields = '__all__'
    success_url = reverse_lazy('inst')


class InstUpdateView(UpdateView):
    model = BookInstance
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    success_url = reverse_lazy('all-borrowed')


class InstDeleteView(DeleteView):
    model = BookInstance
    success_url = reverse_lazy('inst')
