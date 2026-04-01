import json
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import CarService

# 1. Configure Gemini API
# Make sure GEMINI_API_KEY is defined in your settings.py or .env
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def index(request):
    """Renders the main chat interface."""
    return render(request, 'chatbot/index.html')

@csrf_exempt
def chatbot_response(request):
    """Handles the AI logic and database interaction."""
    if request.method == "POST":
        try:
            # Parse user message
            data = json.loads(request.body)
            user_msg = data.get("message", "")

            # 2. Fetch your specific services from the database
            # This ensures the AI only recommends what YOU offer
            db_services = list(CarService.objects.all().values('name', 'price'))
            
            # 3. Create the 'System Instruction' for Gemini
            # We tell the AI exactly how to behave and what data to use
            system_instruction = (
                f"You are a professional Car Service Assistant. "
                f"Our available services and prices are: {db_services}. "
                "Step 1: Greet the user and ask which service they need. "
                "Step 2: Once they pick a service, show the price and ask for their location. "
                "Step 3: After they provide a location, confirm the appointment. "
                "Be polite and concise. If they ask for a service we don't have, kindly say no."
            )

            # 4. Generate the response
            # We combine the instructions with the user message
            full_prompt = f"{system_instruction}\n\nUser Message: {user_msg}"
            response = model.generate_content(full_prompt)

            return JsonResponse({
                "reply": response.text,
                "status": "success"
            })

        except Exception as e:
         return JsonResponse({"reply": f"Actual Error: {str(e)}"})


    return JsonResponse({"error": "Invalid request method"}, status=400)
