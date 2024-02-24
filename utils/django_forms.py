import re

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


def is_positive_number(value):
    value
    try:
        number_string = float(value)

    except ValueError:
        print("Invalid")
        return False

    return number_string > 0
