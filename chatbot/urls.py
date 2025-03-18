from django.urls import path
from .views import chatbot_response, chatbot_page

urlpatterns = [
    path("", chatbot_page, name="chat_page"),  # UI page
    path("api/", chatbot_response, name="chatbot_api"),  # API endpoint
]
