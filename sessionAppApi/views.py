from django.http import JsonResponse

from rest_framework import viewsets

from SessionApp.models import Session

from .serializers import SessionSerializer


def health_check(request):
    """
    Light-weight endpoint so the new app has an addressable route.
    Replace with real API views later.
    """
    return JsonResponse({"status": "ok", "app": "sessionAppApi"})


class SessionViewSet(viewsets.ModelViewSet):
    """
    Expose CRUD operations for Session via REST endpoints.
    """

    queryset = Session.objects.select_related('conference').all()
    serializer_class = SessionSerializer
    filterset_fields = {
        'session_day': ['exact', 'gte', 'lte'],
        'topic': ['exact', 'icontains'],
        'conference': ['exact'],
    }
    search_fields = ['title', 'topic', 'room']
    ordering_fields = ['session_day', 'start_time', 'title']
    ordering = ['session_day', 'start_time']
