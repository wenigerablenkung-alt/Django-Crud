from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "priority", "status"]

    @action(detail=False, methods=["get"])
    def stats(self, request):
        total = Task.objects.count()
        by_status = {
            s: Task.objects.filter(status=s).count() for s, _ in Task.STATUS_CHOICES
        }
        by_priority = {
            p: Task.objects.filter(priority=p).count() for p, _ in Task.PRIORITY_CHOICES
        }
        return Response(
            {"total": total, "by_status": by_status, "by_priority": by_priority}
        )
