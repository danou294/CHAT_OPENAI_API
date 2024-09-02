from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
def create_checkout_session(request):
    print('Creating checkout session...')
    try:
        data = json.loads(request.body)
        price_id = data.get('price_id', 'default_price_id')  # Utilisation des données JSON

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/success/?session_id={CHECKOUT_SESSION_ID}'),
            cancel_url=request.build_absolute_uri('/cancel/')
        )
        return JsonResponse({'id': checkout_session.id})  # Envoyer l'ID de session pour redirection côté client
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def webhook_received(request):
    payload = request.body
    sig_header = request.headers.get('stripe-signature')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    except Exception:
        return JsonResponse({'error': 'Bad request'}, status=400)

    # Process the event
    if event['type'] == 'checkout.session.completed':
        print('Payment succeeded!')
        # Add business logic here

    return JsonResponse({'status': 'success'})
