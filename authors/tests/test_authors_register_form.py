from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
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


class AuthorRegistrationFormIntegrationTestCase(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'email@gmail.com',
            'password': 'Ab123456789',
            'password2': 'Ab123456789',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty.'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Repeat Password must not be empty'),
        ('email', "Email is required")
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        post_url = reverse('authors:create')
        response = self.client.post(post_url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_password2_is_not_equal_to_password(self):
        self.form_data['password'] = "Ab123456789tr"
        post_url = reverse('authors:create')
        response = self.client.post(post_url, data=self.form_data, follow=True)
        msg = "passaword and password2 must be equal"
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_invalid(self):
        self.form_data['password'] = "abc123456789"
        post_url = reverse('authors:create')
        response = self.client.post(post_url, data=self.form_data, follow=True)

        self.assertIn(
            (
                'Password must be at least one uppercase letter, '
                'one lowercase letter and one number. The length should be '
                'at least 8 characters.'
            ),
            response.context['form'].errors.get('password'))

    def test_password_is_value_password(self):
        self.form_data['password'] = "password A1"
        post_url = reverse('authors:create')
        response = self.client.post(post_url, data=self.form_data, follow=True)

        self.assertIn("Don't type password in the password field",
                      response.context['form'].errors.get('password'))

    def test_username_filed_max_length_should_be_150(self):
        self.form_data['username'] = "A" * 160
        post_url = reverse('authors:create')
        response = self.client.post(post_url, data=self.form_data, follow=True)
        self.assertIn(('Certifique-se de que o valor tenha no máximo 150'
                       ' caracteres (ele possui 160).'),
                      response.context['form'].errors.get('username'))

    def test_form_is_valid(self):
        post_url = reverse('authors:create')
        response = self.client.post(post_url, data=self.form_data, follow=True)
        msg = "Your user is created successfully, please log in."
        self.assertIn(msg, response.content.decode('utf-8'))
