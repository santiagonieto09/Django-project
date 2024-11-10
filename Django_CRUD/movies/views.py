from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Movie, UserMovieRating
from .forms import MovieForm, UserMovieRatingForm
from .signals import update_movie_rating

# Create your views here.

def admin_home(request):
    """
    Renderiza la página de inicio del panel de administrador.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Una respuesta HTTP que renderiza la plantilla 'admin_home.html' para el panel de administrador.
    """
    
    return render(request, 'admin_home.html')


def user_home(request):
    """
    Renderiza la página de inicio del usuario.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Una respuesta HTTP que renderiza la plantilla 'user_home.html' para el usuario.
    """
    return render(request, 'user_home.html')


def signup(request):
    """
    Maneja el registro de nuevos usuarios.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Una respuesta HTTP que renderiza la plantilla 'signup.html' con un formulario de registro.
                    Si el registro es exitoso, redirige al usuario a la página de películas disponibles.
                    Si hay errores en el registro, vuelve a renderizar el formulario con los mensajes de error correspondientes.
    """
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('user_available_movies')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Username already exists.'})
        return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Password did not match.'})
 
       
def signin(request):
    """
    Maneja el inicio de sesión de usuarios existentes.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Una respuesta HTTP que renderiza la plantilla 'signin.html' con un formulario de inicio de sesión.
                    Si el inicio de sesión es exitoso y el usuario es un superusuario, redirige a la página de películas del administrador.
                    Si el inicio de sesión es exitoso y el usuario no es un superusuario, redirige a la página de películas disponibles para usuarios normales.
                    Si hay errores en el inicio de sesión, vuelve a renderizar el formulario con los mensajes de error correspondientes.
    """
    error = None
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            error = 'Username or Password is incorrect.'
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': error})
        else:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_movies')
            else:
                login(request, user)
                return redirect('user_available_movies')


@login_required
def signout(request):
    """
    Cierra la sesión del usuario actual y redirige a la página de inicio.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponseRedirect: Una redirección a la página de inicio ('user_home').
    """
    logout(request)
    return redirect('user_home')


@login_required
def admin_movies(request):
    """
    Renderiza la página de administración de películas con todas las películas disponibles ordenadas por título.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Una respuesta que renderiza la plantilla 'admin_movies.html' con las películas disponibles
      ordenadas por título.
    """
    movies = Movie.objects.all().order_by('title')  # Obtener todas las películas disponibles ordenadas por título
    return render(request, 'admin_movies.html', {'movies': movies})


@login_required
def create_movie(request):
    """
    Renderiza el formulario para crear una nueva película o procesa la solicitud POST para crear una nueva película.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Una respuesta que renderiza el formulario 'admin_create_movie.html' para crear una nueva película
      o redirige a la página de administración de películas si la película se crea con éxito.
    """
    
    error = None
    confirmation = None
    
    if request.method == 'GET':
        # Si la solicitud es GET, renderiza el formulario vacío para crear una nueva película
        form = MovieForm()
        return render(request, 'admin_create_movie.html', {'form': form})
    elif request.method == 'POST':
        # Si la solicitud es POST, procesa los datos del formulario para crear una nueva película
        form = MovieForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guarda la película y redirige a la página de administración de películas
            movie = form.save(commit=False)
            movie.save()
            confirmation = 'Successfully created movie.'
            error = 'Please provide valid data.'
            movies = Movie.objects.all().order_by('title')
            return render(request, 'admin_movies.html', {'movies':movies ,'confirmation': confirmation})
        else:
            # Si el formulario no es válido, vuelve a renderizar el formulario con un mensaje de error
            return render(request, 'admin_create_movie.html', {'form': form, 'error': error})

              
@login_required
def admin_movie_detail(request, movie_id):
    """
    Muestra los detalles de una película para editarla o procesa los datos del formulario para actualizarla.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.
    - movie_id: int, el ID de la película a mostrar y editar.

    Returns:
    - HttpResponse: Una respuesta que renderiza el formulario 'admin_movie_detail.html' para editar los detalles de la película
      o redirige a la página de administración de películas si la película se actualiza con éxito.
    """
    # Obtener la película con el ID especificado o mostrar un error 404 si no existe
    movie = get_object_or_404(Movie, pk=movie_id)
    confirmation = None
    error = None
    
    if request.method == 'GET':
        # Si la solicitud es GET, renderiza el formulario para editar los detalles de la película
        form = MovieForm(instance=movie)
        return render(request, 'admin_movie_detail.html', {'movie': movie, 'form': form,'confirmation': confirmation})
    else:
        # Si la solicitud es POST, procesa los datos del formulario para actualizar la película
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            # Si el formulario es válido, guarda los cambios y redirige a la página de administración de películas
            form.save()
            movies = Movie.objects.all().order_by('title')  # Obtener todas las películas disponibles ordenadas por título
            confirmation = 'Successfully modified movie.'
            return render(request, 'admin_movies.html', {'movies': movies, 'confirmation': confirmation})
        else:
            error = 'An unexpected error has occurred.'
            # Si el formulario no es válido, vuelve a renderizar el formulario con un mensaje de error
            return render(request, 'admin_movie_detail.html', {'movie': movie, 'form': form, 'error' : error})

        
@login_required
def delete_movie(request, movie_id):
    """
    Elimina una película específica si el usuario actual es un superusuario.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.
    - movie_id: int, el ID de la película a eliminar.

    Returns:
    - HttpResponse: Redirige a la página de administración de películas si la película se elimina con éxito.
      Renderiza el detalle de la película con un mensaje de error si el usuario no es un superusuario o la solicitud no es POST.
    """
    # Obtener la película con el ID especificado o mostrar un error 404 si no existe
    movie = get_object_or_404(Movie, pk=movie_id)
    confirmation = None
    
        # Eliminar la película si la solicitud es POST
    if request.method == 'POST':
        movie.delete()
        confirmation = 'Movie successfully removed.'
        movies = Movie.objects.all().order_by('title')
        return render(request, 'admin_movies.html', {'movies':movies ,'confirmation': confirmation})
   
    
    
@login_required
def user_available_movies(request):
    """
    Muestra todas las películas disponibles ordenadas por título.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Renderiza la página 'user_available_movies.html' con todas las películas disponibles
      ordenadas por título.
    """
    # Obtener todas las películas disponibles ordenadas por título
    movies = Movie.objects.all().order_by('title')

    # Renderizar la plantilla con las películas disponibles
    return render(request, 'user_available_movies.html', {'movies': movies})
    

@login_required
def user_movie_detail(request, movie_id):
    """
    Muestra los detalles de una película y permite al usuario actualizar la información.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.
    - movie_id: int, el ID de la película.

    Returns:
    - HttpResponse: Renderiza la página 'user_movie_detail.html' con los detalles de la película y un formulario para actualizar la información.
    - Redirect: Redirige a la página 'user_movies' si se actualiza con éxito la información de la película.
    """
    # Obtener la película por su ID o devolver un error 404 si no existe
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'GET':
        # Mostrar los detalles de la película
        return render(request, 'user_movie_detail.html', {'movie': movie})
        
        
@login_required
def add_to_my_list(request, movie_id):
    """
    Agrega una película a la lista de películas del usuario.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.
    - movie_id: int, el ID de la película a agregar a la lista del usuario.

    Returns:
    - HttpResponse: Renderiza la página 'user_movie_detail.html' con un mensaje de error si la película ya está en la lista del usuario.
    - Redirect: Redirige a la página 'user_available_movies' después de agregar la película a la lista del usuario.
    """
    error = None
    
    # Obtener la película seleccionada por su ID o devolver un error 404 si no existe
    movie = get_object_or_404(Movie, pk=movie_id)

    # Verificar si el usuario ya tiene la película en su lista
    user_movie_rating, created = UserMovieRating.objects.get_or_create(user=request.user, movie=movie)

    # Si la relación ya existe, mostrar un mensaje de error
    if not created:
        error = 'This movie is already in your list.'
        return render(request, 'user_movie_detail.html', {'movie': movie, 'error': error})

    movies = Movie.objects.all().order_by('title')
    confirmation = 'Movie successfully added.'
    # Si la relación se crea correctamente, redirigir al usuario a su lista de películas
    return render(request, 'user_available_movies.html', {'movies': movies, 'confirmation': confirmation})


@login_required
def user_movies(request):
    """
    Retorna las películas disponibles para el usuario actual.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Renderiza la página 'user_movies.html' con la lista de películas disponibles para el usuario.
    """
    
    # Filtrar las relaciones UserMovieRating para el usuario dado
    movies = UserMovieRating.objects.filter(user=request.user)
    
    # Obtener las películas asociadas a las relaciones filtradas y ordenarlas por título
    user_movies = [user_movie.movie for user_movie in movies]
    user_movies_sorted = sorted(user_movies, key=lambda movie: movie.title)
    
    return render(request, 'user_movies.html', {'user_movies': user_movies_sorted})


@login_required
def user_movie_delete(request, movie_id):
    """
    Elimina una película de la lista de películas del usuario.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.
    - movie_id: int, el ID de la película que se va a eliminar de la lista del usuario.

    Returns:
    - HttpResponse: Redirige al usuario a la página 'user_movies' después de eliminar la película.
    """
    if request.method == 'POST':
        # Obtener la relación UserMovieRating correspondiente al usuario y la película dada
        user_movie_rating = get_object_or_404(UserMovieRating, user=request.user, movie_id=movie_id)
        
        # Eliminar la relación
        user_movie_rating.delete()
        
        movies = Movie.objects.all().order_by('title')
        confirmation = 'Movie successfully removed from your list.'
        
    
        # Filtrar las relaciones UserMovieRating para el usuario dado
        movies = UserMovieRating.objects.filter(user=request.user)
        
        # Obtener las películas asociadas a las relaciones filtradas y ordenarlas por título
        user_movies = [user_movie.movie for user_movie in movies]
        user_movies_sorted = sorted(user_movies, key=lambda movie: movie.title)
        
        return render(request, 'user_movies.html', {'user_movies': user_movies_sorted, 'confirmation':confirmation})
 
   
@login_required
def user_movie_rating(request, movie_id):
    """
    Permite al usuario calificar una película y guarda la calificación en la base de datos.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.
    - movie_id: int, el ID de la película que se está calificando.

    Returns:
    - HttpResponse: Redirige al usuario a la página 'user_available_movies' después de calificar la película.
    """
    # Obtener la película correspondiente al ID dado
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Obtener o crear una instancia de UserMovieRating para el usuario y la película dada
    user_movie_rating, created = UserMovieRating.objects.get_or_create(user=request.user, movie=movie)

    if request.method == 'GET':
        # Si la solicitud no es un POST, mostrar el formulario de calificación
        form = UserMovieRatingForm(instance=user_movie_rating)
       

    # Renderizar la plantilla 'user_movie_rating.html' con el formulario y la película
    return render(request, 'user_movie_rating.html', {'movie': movie, 'form': form})


@login_required
def user_movie_rate(request, movie_id):
    """
    Permite al usuario calificar una película y actualiza la calificación en la base de datos.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.
    - movie_id: int, el ID de la película que se está calificando.

    Returns:
    - HttpResponse: Redirige al usuario a la página 'user_movies' después de calificar la película.
    """
    if request.method == 'POST':
        # Si la solicitud es un POST, procesar la calificación de la película
        movie = get_object_or_404(Movie, pk=movie_id)
        rating = request.POST.get('rating')
        
        # Obtener o crear la entrada de calificación del usuario para esta película
        user_rating, created = UserMovieRating.objects.get_or_create(user=request.user, movie=movie)
        
        # Actualizar la calificación del usuario para la película
        user_rating.rating = rating
        user_rating.save()
        
        # Actualizar la calificación de la película en el modelo Movie
        update_movie_rating(None, user_rating)
        
        confirmation = 'Movie rated with success.'
    
        # Filtrar las relaciones UserMovieRating para el usuario dado
        movies = UserMovieRating.objects.filter(user=request.user)
        
        # Obtener las películas asociadas a las relaciones filtradas y ordenarlas por título
        user_movies = [user_movie.movie for user_movie in movies]
        user_movies_sorted = sorted(user_movies, key=lambda movie: movie.title)
        
        # Redirigir al usuario a su lista de películas después de calificar
        return render(request, 'user_movies.html', {'user_movies': user_movies_sorted, 'confirmation':confirmation})
    
    
    # Si la solicitud no es un POST, simplemente redirigir al usuario a su lista de películas
    return redirect('user_movies')


@login_required
def search_results(request):
    """
    Retorna los resultados de búsqueda según el título de la película.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Renderiza la página de resultados de búsqueda con las películas encontradas.
    """
    
    error = None
    
    # Obtener el término de búsqueda de la URL
    query = request.GET.get('search_query')

    # Filtrar las películas por título que contenga el término de búsqueda
    movies = Movie.objects.filter(title__icontains=query).order_by('title')

    if not movies:
        error = 'No results found.'
        
    # Determinar el tipo de usuario y renderizar la página correspondiente
    if request.user.is_superuser:
        return render(request, 'admin_movies.html', {'movies': movies,'error': error})
    else:
        return render(request, 'user_available_movies.html', {'movies': movies,'error': error})
 
   
@login_required
def search_from_my_movies(request):
    """
    Realiza una búsqueda de películas dentro de las películas disponibles para el usuario actual.

    Parameters:
    - request: HttpRequest, la solicitud HTTP recibida.

    Returns:
    - HttpResponse: Renderiza la página de películas del usuario con las películas que coinciden con la búsqueda.
    """
    error = None
    
    # Obtener el término de búsqueda de la URL
    query = request.GET.get('search_query')
    
    # Buscar películas en base a la consulta
    movies = Movie.objects.filter(title__icontains=query).values_list('id', flat=True).order_by('title')
    
    # Filtrar las películas encontradas por el usuario actual en UserMovieRating
    user_movies = UserMovieRating.objects.filter(user=request.user, movie_id__in=movies)
    
    # Obtener las películas que coinciden con las IDs encontradas
    movies = Movie.objects.filter(id__in=user_movies.values_list('movie_id', flat=True))
    
    if not movies:
        error = 'No results found.'
    
    return render(request, 'user_movies.html', {'user_movies': movies, 'error': error})