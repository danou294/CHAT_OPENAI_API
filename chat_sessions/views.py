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

# Importer les fonctions nécessaires depuis chat_messages.views
from chat_messages.views import send_to_openai, generate_conversation_title

@require_http_methods(["POST"])
@csrf_exempt
def create_session(request):
    try:
        data = json.loads(request.body)
        participant_id = data.get('participant_id')
        if not participant_id:
            return JsonResponse({'error': 'ID de participant requis.'}, status=400)
        session = ChatSession.objects.create(participant_id=participant_id)
        return JsonResponse({'session': {'id': session.id, 'participant_id': session.participant_id, 'title': 'Nouvelle conversation', 'created_at': session.created_at}}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides.'}, status=400)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_sessions(request):
    participant_id = request.GET.get('participant_id')  # Récupérer l'ID utilisateur depuis les paramètres GET
    if not participant_id:
        return JsonResponse({'error': 'ID de participant requis.'}, status=400)
    sessions = ChatSession.objects.filter(participant_id=participant_id).order_by('-created_at')
    sessions_data = []
    for session in sessions:
        sessions_data.append({
            'id': session.id,
            'participant_id': session.participant_id,
            'title': session.title or "Nouvelle conversation",
            'created_at': session.created_at
        })
    return JsonResponse({'sessions': sessions_data})

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_session(request, session_id):
    session = get_object_or_404(ChatSession, pk=session_id)
    session.delete()
    return JsonResponse({'message': 'La session a été supprimée avec succès.'}, status=204)

@require_http_methods(["POST"])
@csrf_exempt
def create_conversation_with_message(request):
    """Crée une nouvelle conversation et envoie le premier message avec génération du titre"""
    print(f"🔵 [DJANGO] create_conversation_with_message appelé")
    try:
        data = json.loads(request.body)
        print(f"🔵 [DJANGO] Données reçues: {data}")
        
        participant_id = data.get('participant_id')
        content = data.get('content')
        sender_id = data.get('sender_id')
        temperature = data.get('temperature', 0.7)

        if not participant_id or not content or not sender_id:
            return JsonResponse({'error': 'participant_id, content et sender_id requis.'}, status=400)

        # Créer la nouvelle session
        session = ChatSession.objects.create(participant_id=participant_id)
        print(f"✅ [DJANGO] Nouvelle session créée: {session.id}")

        # Générer le titre basé sur le premier message
        print(f"🔵 [DJANGO] Génération du titre pour la session {session.id}")
        try:
            generated_title = generate_conversation_title(content)
            session.title = generated_title
            session.save()
            print(f"✅ [DJANGO] Titre généré: {generated_title}")
        except Exception as e:
            print(f"❌ [DJANGO] Erreur génération titre: {str(e)}")
            session.title = "Nouvelle conversation"
            session.save()

        # Créer le message utilisateur
        user_message = Message.objects.create(
            chat_session=session,
            sender_id=sender_id,
            content=content,
            is_from_user=True
        )
        print(f"✅ [DJANGO] Message utilisateur créé: {user_message.id}")

        # Envoyer à OpenAI et obtenir la réponse
        print(f"🔵 [DJANGO] Envoi à OpenAI...")
        response_content = send_to_openai([content], content, temperature)
        print(f"✅ [DJANGO] Réponse OpenAI reçue: {response_content[:50]}...")
        
        # Créer le message de réponse d'OpenAI
        ai_message = Message.objects.create(
            chat_session=session,
            sender_id='openai',
            content=response_content,
            is_from_user=False,
            is_sent_to_openai=True
        )
        print(f"✅ [DJANGO] Message IA créé: {ai_message.id}")

        # Retourner la session avec les messages
        updated_messages = Message.objects.filter(chat_session=session).order_by('timestamp')
        message_list = list(updated_messages.values('id', 'sender_id', 'content', 'timestamp', 'is_from_user'))
        
        return JsonResponse({
            'session': {
                'id': session.id,
                'participant_id': session.participant_id,
                'title': session.title,
                'created_at': session.created_at
            },
            'messages': message_list
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides.'}, status=400)
    except Exception as e:
        print(f"❌ [DJANGO] Erreur générale: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def add_message(request, session_id):
    print(f"🔵 [DJANGO] add_message appelé pour session {session_id}")
    try:
        data = json.loads(request.body)
        print(f"🔵 [DJANGO] Données reçues: {data}")
        
        chat_session = get_object_or_404(ChatSession, pk=session_id)
        print(f"🔵 [DJANGO] Session trouvée: {chat_session.id}")
        
        content = data.get('content')
        sender_id = data.get('sender_id')
        is_from_user = data.get('is_from_user', True)
        temperature = data.get('temperature', 0.7)

        print(f"🔵 [DJANGO] Contenu: {content[:50]}..., Sender: {sender_id}, User: {is_from_user}")

        if not content or not sender_id:
            print(f"❌ [DJANGO] Données manquantes: content={bool(content)}, sender_id={bool(sender_id)}")
            return JsonResponse({'error': 'Contenu et ID de l\'expéditeur requis.'}, status=400)

        # Création du message utilisateur
        print(f"🔵 [DJANGO] Création du message utilisateur...")
        message = Message.objects.create(
            chat_session=chat_session,
            sender_id=sender_id,
            content=content,
            is_from_user=is_from_user
        )
        print(f"✅ [DJANGO] Message utilisateur créé avec ID: {message.id}")

        # Obtenir le contexte des messages précédents pour la session
        context_messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp').values_list('content', flat=True)
        print(f"🔵 [DJANGO] Contexte: {len(context_messages)} messages précédents")

        # Envoyer le message à OpenAI et obtenir la réponse
        if is_from_user:
            print(f"🔵 [DJANGO] Envoi à OpenAI...")
            response_content = send_to_openai(list(context_messages), content, temperature)
            print(f"✅ [DJANGO] Réponse OpenAI reçue: {response_content[:50]}...")
            
            # Création du message de réponse d'OpenAI
            ai_message = Message.objects.create(
                chat_session=chat_session,
                sender_id='openai',
                content=response_content,
                is_from_user=False,
                is_sent_to_openai=True
            )
            print(f"✅ [DJANGO] Message IA créé avec ID: {ai_message.id}")

        # Retourner les messages mis à jour
        updated_messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')
        message_list = list(updated_messages.values('id', 'sender_id', 'content', 'timestamp', 'is_from_user'))
        print(f"✅ [DJANGO] Retour de {len(message_list)} messages")
        return JsonResponse({'messages': message_list}, status=201)
    except json.JSONDecodeError:
        print(f"❌ [DJANGO] Erreur JSON decode")
        return JsonResponse({'error': 'Données JSON invalides.'}, status=400)
    except Exception as e:
        print(f"❌ [DJANGO] Erreur générale: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    message.delete()
    return JsonResponse
