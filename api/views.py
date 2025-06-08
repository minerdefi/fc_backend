from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def home(request):
    return JsonResponse({"message": "Hello AG!"})

def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return JsonResponse({
        "status": "healthy",
        "message": "FG Premium backend is running"
    })
