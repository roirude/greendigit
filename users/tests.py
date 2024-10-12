from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.email = "user@test.com"
        self.password = "securepwd"
        self.is_consumer = True
        self.country = "cameroon"
        
    def test_successful_signup_and_email_confirmation(self):
        response = self.client.post(reverse('account_signup'), {
            'email' : self.email,
            'password1' : self.password,
            'password2' : self.password,
            'is_consumer' : self.is_consumer,
            'country' : self.country
        })
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(len(mail.outbox), 1)
        confirmation_email = mail.outbox[0]
        self.assertIn(self.email, confirmation_email.to)
        
        url_start = confirmation_email.body.find('/accounts/confirm-email/')
        url_end = confirmation_email.body.find('\n', url_start)
        confirmation_url = confirmation_email.body[url_start:url_end].strip()
        
        response = self.client.get(confirmation_url)
        self.assertEqual(response.status_code, 302)
        
        response = self.client.post(reverse('account_login'), {
            'login' : self.email,
            'password' : self.password, 
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

