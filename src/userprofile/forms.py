from django import forms


class WishForm(forms.Form):

    title = forms.CharField(
        label=None,
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Название'})
    )

    link = forms.URLField(
        label=None,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ссылка'})
    )

    description = forms.CharField(
        label=None,
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Описание'})
    )

    type = forms.CharField(
        label=None,
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Раздел'})
    )

    image = forms.FileField(
        label=None,
        required=False,
        widget=forms.FileInput(attrs={'placeholder': 'Изображение'})
    )
