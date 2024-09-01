from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from chat_sessions.models import ChatSession
from chat_messages.models import Message
from django.core.exceptions import ValidationError
import json
import openai
import os

@require_http_methods(["POST"])
@csrf_exempt
def create_session(request):
    try:
        data = json.loads(request.body)
        participant_id = data.get('participant_id')
        if not participant_id:
            return JsonResponse({'error': 'ID de participant requis.'}, status=400)
        session = ChatSession.objects.create(participant_id=participant_id)
        return JsonResponse({'session': {'id': session.id, 'participant_id': session.participant_id, 'created_at': session.created_at}}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides.'}, status=400)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_sessions(request):
    participant_id = request.GET.get('participant_id')  # Récupérer l'ID utilisateur depuis les paramètres GET
    if not participant_id:
        return JsonResponse({'error': 'ID de participant requis.'}, status=400)
    sessions = ChatSession.objects.filter(participant_id=participant_id)
    return JsonResponse({'sessions': list(sessions.values('id', 'participant_id', 'created_at'))})

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_session(request, session_id):
    session = get_object_or_404(ChatSession, pk=session_id)
    session.delete()
    return JsonResponse({'message': 'La session a été supprimée avec succès.'}, status=204)

@require_http_methods(["POST"])
@csrf_exempt
def add_message(request, session_id):
    try:
        data = json.loads(request.body)
        chat_session = get_object_or_404(ChatSession, pk=session_id)
        content = data.get('content')
        sender_id = data.get('sender_id')
        is_from_user = data.get('is_from_user', True)
        temperature = data.get('temperature', 0.7)

        if not content or not sender_id:
            return JsonResponse({'error': 'Contenu et ID de l\'expéditeur requis.'}, status=400)

        # Création du message utilisateur
        message = Message.objects.create(
            chat_session=chat_session,
            sender_id=sender_id,
            content=content,
            is_from_user=is_from_user
        )

        # Obtenir le contexte des messages précédents pour la session
        context_messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp').values_list('content', flat=True)

        # Envoyer le message à OpenAI et obtenir la réponse
        if is_from_user:
            response_content = send_to_openai(list(context_messages), content, temperature)
            # Création du message de réponse d'OpenAI
            Message.objects.create(
                chat_session=chat_session,
                sender_id='openai',
                content=response_content,
                is_from_user=False,
                is_sent_to_openai=True
            )

        # Retourner les messages mis à jour
        updated_messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')
        message_list = list(updated_messages.values('id', 'sender_id', 'content', 'timestamp', 'is_from_user'))
        return JsonResponse({'messages': message_list}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    message.delete()
    return JsonResponse
