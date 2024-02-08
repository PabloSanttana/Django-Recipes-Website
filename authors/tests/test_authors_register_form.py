from unittest import TestCase

from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegistrationFormUnitTest(TestCase):

    # Fazendo validacoes de placeholder
    @parameterized.expand([
        ('email', 'Your e-mail'),
        ('username', 'Your username'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: wick'),
        ('password2', 'Repeat your password'),
        ('password', 'Your password'),
    ])
    def test_fields_placeholder_is_corrects(self, field, placeholder_value):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_value, placeholder)

    # fazendo validacoes de help_text

    @parameterized.expand([
        ('username', ('Required. 150 characters or fewer. Letters, numbers,'
                      ' and @/./+/-/_ only.')),
        ('email', 'The e-mail must be a valid email address'),
        ('password', ('Password must be at least one uppercase letter, '
                      'one lowercase letter and one number. The length should'
                      ' be at least 8 characters.')),
    ])
    def test_fields_help_text_is_corrects(self, field, help_text_value):
        form = RegisterForm()
        help_text = form[field].field.help_text
        self.assertEqual(help_text_value, help_text)

    # Fazendo validacoes de Label

    @parameterized.expand([
        ('email', 'Email'),
        ('username', 'Username'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('password2', 'Repeat password'),
        ('password', 'Password'),
    ])
    def test_fields_label_is_corrects(self, field, label_value):
        form = RegisterForm()
        label = form[field].field.label
        self.assertEqual(label_value, label)
