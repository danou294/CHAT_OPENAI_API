from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import stripe

# Configuration du logger
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutView(APIView):
    def post(self, request):
        logger.info('Received POST request to create checkout session: %s', request.data)

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,  
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='subscription',
                success_url=f"{settings.SITE_URL}/premium-offer?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.SITE_URL}/premium-offer?canceled=true",
            )
            logger.info('Stripe Checkout Session created successfully: %s', checkout_session.id)
            return Response({'url': checkout_session.url})
        except stripe.error.StripeError as e:
            logger.error('Stripe error occurred: %s', e.error.message)
            return Response(
                {'error': f'Stripe error: {e.error.message} (request ID: {e.request_id})'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error('An error occurred: %s', str(e))
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
