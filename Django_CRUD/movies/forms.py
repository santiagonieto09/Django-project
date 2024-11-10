from django import forms
from .models import Movie, UserMovieRating

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'director', 'release_year', 'duration', 'age_rating', 'genre', 'image_url', 'trailer_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Description'}),
            'director': forms.TextInput(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Director'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Release Year'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Duration (minutes)'}),
            'age_rating': forms.TextInput(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Age Rating'}),
            'genre': forms.TextInput(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Genre'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Image URL'}),
            'trailer_url': forms.URLInput(attrs={'class': 'form-control bg-secondary bg-gradient', 'placeholder': 'Trailer URL'}),
        }


class UserMovieRatingForm(forms.ModelForm):
    class Meta:
        model = UserMovieRating
        fields = ['rating']