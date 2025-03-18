from django.shortcuts import render
import os
from django.http import JsonResponse
import google.generativeai as genai
from decouple import config

# Configure Gemini API with the key from .env
genai.configure(api_key=config("GEMINI_API_KEY"))

def chatbot_page(request):
    return render(request, "chatbot/chat.html")

def chatbot_response(request):
    """Handles user messages and generates AI responses."""
    user_message = request.GET.get("message", "")

    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(user_message)

    return JsonResponse({"response": response.text})

# Create your views here.
