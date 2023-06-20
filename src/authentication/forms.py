from django import forms

import authentication.message_text


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )

    email = forms.EmailField(
        required=True, label="", widget=forms.TextInput(attrs={"placeholder": "Email"})
    )

    password = forms.CharField(
        required=True,
        initial="",
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}),
    )
    confirm_password = forms.CharField(
        required=True,
        initial="",
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтверждение пароля"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["password"] != cleaned_data["confirm_password"]:
            self.add_error(
                "confirm_password",
                authentication.message_text.not_equals_password_confirm_password,
            )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
    )

    password = forms.CharField(
        required=True,
        initial="",
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}),
    )


class EmailForm(forms.Form):
    email = forms.EmailField(
        required=True, label="", widget=forms.TextInput(attrs={"placeholder": "Email"})
    )


class VerificationCodeForm(forms.Form):
    verification_code = forms.IntegerField(
        max_value=9999,
        min_value=1000,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Код из письма"}),
    )


class NewPasswordForm(forms.Form):
    password = forms.CharField(
        required=True,
        initial="",
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}),
    )

    confirm_password = forms.CharField(
        required=True,
        initial="",
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}),
    )

    verification_code = forms.IntegerField(
        max_value=9999,
        min_value=1000,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Код из письма"}),
    )
