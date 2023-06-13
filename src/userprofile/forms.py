from django import forms

from .models import Wish


class WishForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Wish
        fields = ("title", "link", "description", "type")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Название"}),
            "link": forms.TextInput(attrs={"placeholder": "Ссылка"}),
            "description": forms.Textarea(attrs={"placeholder": "Описание", "rows": 4}),
            "type": forms.TextInput(attrs={"placeholder": "Раздел"}),
        }
