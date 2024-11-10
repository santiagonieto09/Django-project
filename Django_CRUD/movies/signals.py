from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserMovieRating
from django.db.models import Avg

# Definimos una función para calcular y actualizar el campo `rating` en el modelo `Movie`
def update_movie_rating(sender, instance, **kwargs):
    """
    Esta función calcula el promedio de las calificaciones de una película y actualiza su campo `rating`.
    
    Argumentos:
        sender: El modelo que emitió la señal (UserMovieRating en este caso).
        instance: La instancia de UserMovieRating que activó la señal.
        **kwargs: Otros argumentos adicionales pasados a la función.
    """
    # Obtenemos la película asociada a la instancia de UserMovieRating
    movie = instance.movie
    
    # Calculamos el promedio de las calificaciones de la película
    average_rating = UserMovieRating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
    
    # Actualizamos el campo `rating` de la película con el promedio calculado
    movie.rating = average_rating
    movie.save()

# Conectamos la función `update_movie_rating` a las señales `post_save` y `post_delete` del modelo `UserMovieRating`
@receiver(post_save, sender=UserMovieRating)
@receiver(post_delete, sender=UserMovieRating)
def update_movie_rating_on_save_or_delete(sender, instance, **kwargs):
    """
    Esta función conecta la señal post_save y post_delete del modelo UserMovieRating
    a la función update_movie_rating para mantener actualizado el campo `rating` de la película.
    
    Argumentos:
        sender: El modelo que emitió la señal (UserMovieRating en este caso).
        instance: La instancia de UserMovieRating que activó la señal.
        **kwargs: Otros argumentos adicionales pasados a la función.
    """
    # Llamamos a la función update_movie_rating para actualizar el campo `rating`
    update_movie_rating(sender, instance, **kwargs)
