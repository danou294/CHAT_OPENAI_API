from django.http import JsonResponse
from .models import ChatSession
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json

@require_http_methods(["POST"])
@csrf_exempt  # À utiliser avec précaution; il serait préférable d'avoir une authentification API
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
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

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
