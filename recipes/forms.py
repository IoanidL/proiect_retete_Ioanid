from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'prep_time', 'cooking_time']
        labels = {
            'title': 'Titlu',
            'description': 'Preparare',
            'prep_time': 'Timp de pregătire (minute)',
            'cooking_time': 'Timp de gătire (minute)',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Titlul este obligatoriu.")
        if len(title.strip()) < 5:
            raise forms.ValidationError("Titlul trebuie să aibă cel puțin 5 caractere.")
        return title

    def clean_prep_time(self):
        prep_time = self.cleaned_data.get('prep_time')
        if prep_time is None or prep_time <= 0:
            raise forms.ValidationError("Timpul de pregătire trebuie să fie un număr pozitiv.")
        return prep_time

    def clean_cooking_time(self):
        cooking_time = self.cleaned_data.get('cooking_time')
        if cooking_time is None or cooking_time <= 0:
            raise forms.ValidationError("Timpul de gătire trebuie să fie un număr pozitiv.")
        return cooking_time