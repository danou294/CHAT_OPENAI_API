from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock
import json

class StripeTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session(self, mock_create):
        mock_create.return_value = Mock(url='http://testserver/stripe-checkout')
        response = self.client.post(reverse('create_checkout_session'), {'price_id': 'price_123'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/stripe-checkout')

    @patch('stripe.Webhook.construct_event')
    def test_webhook_received(self, mock_construct_event):
        # Configure mock to return a custom Stripe event object
        mock_construct_event.return_value = {
            'type': 'checkout.session.completed',
            'data': {'object': {'session_id': 'sess_123'}}
        }

        # Create JSON data for the POST request
        data = json.dumps({'type': 'checkout.session.completed'})

        # Make POST request with JSON data and custom header
        response = self.client.post(
            reverse('webhook'),
            data=data,
            content_type='application/json',
            **{'HTTP_STRIPE_SIGNATURE': 'signature'}
        )

        # Asserts to check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})
