from django import forms


class RegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=20,
        required=True,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
    )

    email = forms.EmailField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )

    password = forms.CharField(
        required=True,
        initial='',
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )
    confirm_password = forms.CharField(
        required=True,
        initial='',
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля'
        })
    )
