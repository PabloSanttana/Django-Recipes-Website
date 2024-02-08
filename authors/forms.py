import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# funcao para axilixar ao mudar widget


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must be at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ), code='invalid')


def add_attr(field, attr_name, attr_new_value):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_value}'.strip()


def add_placeholder(field, placeholder_value):
    add_attr(field, 'placeholder', placeholder_value)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Your username')
        add_placeholder(self.fields['last_name'], 'Ex.: wick')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_attr(self.fields['email'], "class", "form-control")

    # criando um novo campo ou sobrescrevendo
    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty',
        },
        help_text=(
            'Password must be at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password]

    )
    password2 = forms.CharField(
        required=True,
        label="Repeat password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat your password'
        }),
        error_messages={
            'required': 'Repeat Password must not be empty',
        }
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',

        }

        help_texts = {
            'email': 'The e-mail must be a valid email address',
            'username': ('Required. 150 characters or fewer. Letters, numbers,'
                         ' and @/./+/-/_ only.'),
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty.',
                'invalid': 'This field is invalid.'
            }
        }

        # sobreescrever um input
        # uma forma
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: John'
            }),
        }

    # Fazendo validacao especifica no password

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'password' in data:
            raise ValidationError(
                "Don't type %(value)s in the password field",
                code='invalid',
                params={'value': 'password'}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError(
                {
                    'password': ValidationError(
                        "passaword and password2 must be equal",
                        code='invalid'),
                    'password2':  ValidationError(
                        "passaword and password2 must be equal",
                        code='invalid'),
                }

            )
