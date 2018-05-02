from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID', 'appXE8NjesMdUuPAU'),
            'Movies',
            api_key = os.environ.get('AIRTABLE_API_KEY', 'keya3hGnm0XyQI1d6'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    context_dict = {'search_result': search_result}
    print(user_query)
    return render(request, 'movies/movies_stuff.html', context_dict)

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://www.classicposters.com/images/nopicture.gif'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': str(request.POST.get('notes'))
        }

        try:
            response = AT.insert(data)
            messages.success(request, 'New movie added: {}' .format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Error trying to add a new movie: {}' .format(e))
    return redirect('/')

def update(request, movie_id):
    if request.method == 'POST':
        updated_data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://www.classicposters.com/images/nopicture.gif'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        try:
            response = AT.update(movie_id, updated_data)
            messages.success(request, 'Movie updated: {}' .format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Error trying to update a movie: {}' .format(e))
    return redirect('/')

def delete(request, movie_id):
    if request.method == 'POST':
        try:
            movie_name = AT.get(movie_id)['fields'].get('Name')
            response = AT.delete(movie_id)
            messages.warning(request, 'Movie deleted: {}' .format(movie_name))
        except Exception as e:
            messages.warning(request, 'Error trying to delete a movie: {}' .format(e))
    return redirect('/')
