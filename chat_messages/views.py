from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from chat_sessions.models import ChatSession
from chat_messages.models import Message
import json
import openai
import os

# Fonction pour calculer le nombre de tokens maximum basé sur le contexte et le message
def calculate_max_tokens(context, message):
    total_length = sum(len(m) for m in context) + len(message)
    return min(4096 - total_length, 1000)

# Fonction pour envoyer un message à OpenAI et obtenir une réponse
def send_to_openai(context, message, temperature):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    try:
        max_tokens = calculate_max_tokens(context, message)
        
        # Préparation des messages pour l'API de chat
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.extend({"role": "user", "content": msg} for msg in context)
        messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return str(e)

@require_http_methods(["POST"])
@csrf_exempt
def add_message(request, session_id):
    try:
        data = json.loads(request.body)
        chat_session = get_object_or_404(ChatSession, pk=session_id)
        content = data.get('content')
        sender_id = data.get('sender_id')
        is_from_user = data.get('is_from_user', True)
        temperature = data.get('temperature', 0.7)  # Ajout de la température

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
                sender_id='openai',  # ID d'expéditeur fictif pour OpenAI
                content=response_content,
                is_from_user=False,
                is_sent_to_openai=True
            )

        return JsonResponse({'message': f'Le message a été ajouté avec succès dans la session {session_id}.'}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    message.delete()
    return JsonResponse({'message': 'Le message a été supprimé avec succès.'}, status=204)

@require_http_methods(["GET"])
def get_messages(request, session_id):
    chat_session = get_object_or_404(ChatSession, pk=session_id)
    messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')
    message_list = list(messages.values('id', 'sender_id', 'content', 'timestamp', 'is_from_user'))
    return JsonResponse({'messages': message_list})

@require_http_methods(["POST"])
@csrf_exempt
def create_session(request):
    try:
        data = json.loads(request.body)
        participant_id = data.get('participant_id')
        if not participant_id:
            return JsonResponse({'error': 'ID de participant requis.'}, status=400)
        session = ChatSession.objects.create(participant_id=participant_id)
        return JsonResponse({'message': f'La session {session.id} a été créée avec succès.'}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def list_sessions(request):
    sessions = ChatSession.objects.all()
    return JsonResponse({'sessions': list(sessions.values('id', 'participant_id', 'created_at'))})

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_session(request, session_id):
    session = get_object_or_404(ChatSession, pk=session_id)
    session.delete()
    return JsonResponse({'message': 'La session a été supprimée avec succès.'}, status=204)
