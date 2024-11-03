from django.shortcuts import render, redirect
# chat/views.py

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import chatSessions, chatMessages, Patient  # Assuming you have a Patient model
from django.views.decorators.csrf import csrf_exempt
from .llm_integrations import extract_entities
#, store_in_neo4j
from neo4j import GraphDatabase
# from langchain.llms import OpenAI
import json
import os
# from .models import chatSessions, chatMessages, patient

# llm = OpenAI(open_api_key="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")
# llm = llm_gemini(model_name=os.getenv('MODEL_NAME'))


# Initialize Neo4j Driver
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "keyush06"))

# FitBit/chatbot/views.py
from .models import Patient

def get_patient_details(patient_id=1):
    try:
        # Fetch the patient record from the database
        patient = Patient.objects.get(patient_id=patient_id)
        # Map the result to a dictionary
        return {
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email,
            "phone_number": patient.phone_number,
            "dob": patient.date_of_birth,
            "address": patient.address,
            "medical_condition": patient.medical_condition,
            "medication_regimen": patient.medication_regimen,
            "last_appointment": patient.last_appointment,
            "next_appointment": patient.next_appointment,
            "doctor_name": patient.doctor_name
        }
    except Patient.DoesNotExist:
        return None  # Return None if no patient is found


# Placeholder function to generate bot response
def generate_bot_response(user_message):
    """
    Generate a bot response by analyzing user_message with the LLM.
    
    """

    patient_details = get_patient_details(patient_id=1)

    entities = extract_entities(user_message, patient_details)  # Extract entities from user message
    print("Extracted Entities:", entities)
    
    # Fetch the 'response' value from entities dictionary
    response_text = entities.get("response", "I'm here to assist with health-related inquiries.")
    return response_text

    # entities = extract_entities(user_message)  # Extract entities from user message
    # print("Extracted Entities JSON:", entities)
    
    # # Ensure that only the response text is sent back as a string
    # response_text = entities.get("response", "I'm here to assist with health-related inquiries.").strip().lower()
    
    # return response_text

    # entities = extract_entities(user_message)  # Extract entities from user message
    # print("Extracted Entities JSON:", entities)
    # try:
    #     entities_dict = json.loads(entities)  # Convert JSON string to dictionary
    #     response_text = entities_dict.get("response", "").strip().lower()  # Get the response field
    # except json.JSONDecodeError:
    #     response_text = "I'm here to assist with health-related inquiries."  # Default message in case of error

    # return response_text




    # store_in_neo4j(entities)  # Store extracted entities in Neo4j

    # try:
    #     store_in_neo4j(entities)  # Store extracted entities in Neo4j
    # except Exception as e:
    #     print("Error storing entities in Neo4j:", e)
    #     return "An error occurred while processing your request."

    # Create a response based on entities detected
    # if "appointment_time" in entities:
    #     return "I will convey your request to Dr. [Doctor's Name]."
    # elif "medication" in entities:
    #     return "Please make sure to take your medication as prescribed."
    # elif "medical_condition" in entities:
    #     return "I’m here to help with any health-related inquiries. Feel free to ask."
    # else:
    #     return "I'm here to help with any health-related inquiries."
    
def home(request):
    # Fetch all chat sessions for the sidebar
    chatSessions_list = chatSessions.objects.all()

    # Check if patient with `patient_id=1` exists; if not, create one
    if not Patient.objects.filter(patient_id=1).exists():
        patient_record = Patient.objects.create(
            patient_id=1,
            first_name='keyush',
            last_name='Shah',
            email="ks@gmail.com",
            phone_number='9899822',
            date_of_birth='1999-05-19',
            address='123 Main St, Cityville',
            medical_condition='Hypertension',
            medication_regimen='Medication X',
            allergies='None',
            last_appointment='2024-02-19',
            next_appointment='2024-03-19',
            doctor_name='Dr. Grossman'
        )
    else:
        # If the patient exists, fetch the record
        patient_record = Patient.objects.get(patient_id=1)

    # Check if any chat sessions exist
    if chatSessions_list.exists():
        # Get the last chat session
        selected_session = chatSessions_list.last()
        # Fetch messages for the last session, ordered by message time
        messages = chatMessages.objects.filter(session_id=selected_session).order_by('time_sent')
    else:
        # If no sessions exist, create a new one
        selected_session = chatSessions.objects.create(name="New Chat Session")
        messages = None  # No messages for the new session yet

        # Redirect to the home view to avoid duplicate form submission
        return redirect('home')

    # Render the home template with the necessary context
    return render(request, 'interface.html', {
    'chatSessions_list': chatSessions_list,  # All chat sessions for the sidebar
    'selected_session': selected_session,  # Last session or new session
    'bot_message': messages,  # Messages for the selected session
    # 'summary': patient_record.patient_summary  # Summary from the patient record
})

# View to handle chat session and display chat history
def chat_session_view(request, session_id):
    # Fetch the chat session and related messages
    session = get_object_or_404(chatSessions, id=session_id)
    messages = chatMessages.objects.filter(session_id=session).order_by('time_sent')

    # Retrieve all chat sessions for the sidebar
    chat_sessions_list = chatSessions.objects.all()

    # Fetch patient details (assuming a single patient for simplicity)
    patient = Patient.objects.first()  # Adjust as necessary if multiple patients

    if request.method == 'POST':
        user_message_text = request.POST.get('message')

        user_message = chatMessages.objects.create(
            session_id=session,
            sender="User",
            message=user_message_text,
            time_sent=timezone.now()
        )
        print("checking here")
        
        bot_response_text = generate_bot_response(user_message_text)
        print(bot_response_text)
        bot_message = chatMessages.objects.create(
            session_id=session,
            sender="Bot",
            message=bot_response_text,
            time_sent=timezone.now()
        )

        return JsonResponse({
            'user_message': {
                'message': user_message.message,
                'timestamp': user_message.time_sent.strftime('%Y-%m-%d %H:%M:%S')
            },
            'bot_message': {
                'message': bot_message.message,
                'timestamp': bot_message.time_sent.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    #Conversation summ based on date and time
    conversation_summary = []
    previous_date = None

    for msg in messages:
        current_date = msg.time_sent.date()
        if current_date != previous_date:
            # Add a bold date separator if it's a new day
            conversation_summary.append(f"**{current_date.strftime('%Y-%m-%d')}**")
            previous_date = current_date
        # Add each message with a timestamp
        conversation_summary.append(f"{msg.time_sent.strftime('%H:%M:%S')} - {msg.sender}: {msg.message}")

    # Join the summary with newline characters to separate entries
    formatted_summary = "\n".join(conversation_summary)


    # conversation_summary = "\n".join([
    #     f"{msg.time_sent.strftime('%Y-%m-%d %H:%M:%S')} - {msg.sender}: {msg.message}"
    #     for msg in messages
    # ])

    return render(request, 'interface.html', {
        'session': session,
        'messages': messages,
        'chatSessions_list': chat_sessions_list,
        'selected_session': session,
        'patient': patient,
        'summary': formatted_summary,
    })


def create_chat_session(request):
    # Create a new chat session
    new_session = chatSessions.objects.create(name="New Chat Session")
    
    # Redirect to the chat session page of the newly created session
    return redirect('chat_session', session_id=new_session.id)


@csrf_exempt
def rename_session(request, session_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_name = data.get('new_name', '').strip()

        if new_name:
            try:
                session = chatSessions.objects.get(id=session_id)
                session.name = new_name
                session.save()
                return JsonResponse({'success': True})
            except chatSessions.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Session not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def delete_chat_session(request, session_id):
    session = get_object_or_404(chatSessions, id=session_id)
    session.delete()
    return redirect('home')


