## Integrating the bot's responses with LLMs. I want to make an LLM agnostic modular code so that we can swap the LLMs for the responses.

# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
from openai import OpenAI
import openai
import os
from neo4j import GraphDatabase
import json
from dotenv import load_dotenv
import google.generativeai as genai
import re
# import google.generativeai as genai

# Initialize LLM
# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME")
# client = OpenAI()
print("Using model:", model_name)



# llm = OpenAI(openai_api_key="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")
# llm = OpenAI(openai_api_key="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")

# gemini
class GeminiChat():
    def __init__(self, key, model_name):
        from google.generativeai import client,GenerativeModel
        
        self.api_key = key
        self.model_name = model_name
        genai.configure(api_key=key)
        self.model = GenerativeModel(model_name=self.model_name)
        
        
    def generate_content(self,prompt):
        # from google.generativeai.types import content_types
        try:
            # Call the model to generate content
            response = self.model.generate_content(prompt)
            
            # Print the structure of the response for debugging
            print("Raw response:", response)

            # Check if 'candidates' exists in the response
            if hasattr(response, 'candidates'):
                candidates = response.candidates

                if candidates and hasattr(candidates[0], 'content') and hasattr(candidates[0].content, 'parts'):
                    # Extract the main text content
                    content_text = candidates[0].content.parts[0].text
                    
                    # If the text is wrapped in ```json, strip it
                    if content_text.startswith("```json"):
                        content_text = content_text.strip("```json").strip("```")
                    
                    # Parse the JSON-like content text
                    json_response = json.loads(content_text)
                    return json_response  # JSON-serializable output
                else:
                    return {"error": "No valid content in candidates"}
            else:
                return {"error": "Response does not contain 'candidates' attribute"}
        except Exception as e:
            return "**ERROR**: " + str(e), 0

# OpenAI
class LLMOpenAI:
    def __init__(self, api_key, model_name):
        openai.api_key = api_key  # Set the API key for the openai module
        self.model_name = model_name
        self.client  = openai.Client(api_key=OPENAI_API_KEY)

    def generate_content(self, system_prompt, user_message):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,  # Specify the chat model (e.g., "gpt-3.5-turbo")
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=50,
                temperature=0
            )
            return response.choices[0].message["content"]
        except Exception as e:
            return f"**ERROR**: {str(e)}"


# Initialize Neo4j Driver
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "keyush06"))

def extract_requested_date(user_message):
    # Simple regex to find date-like patterns (e.g., "next Friday", "March 5", "2024-03-05")
    date_patterns = [
        r'\b(\d{4}-\d{2}-\d{2})\b',  # matches dates in YYYY-MM-DD format
        r'\b(\d{2}/\d{2}/\d{4})\b',  # matches dates in MM/DD/YYYY format
        r'\b(\d{1,2}(st|nd|rd|th)?\s+\w+)\b',  # matches dates like "5th March"
        r'\b(next\s+\w+)\b',  # matches phrases like "next Friday"
    ]
    for pattern in date_patterns:
        match = re.search(pattern, user_message, re.IGNORECASE)
        if match:
            return match.group(0)  # Return the matched date string
    return None  # Return None if no date is found

def extract_entities(user_message, patient_details=None):
    requested_date = extract_requested_date(user_message)
    if not requested_date:
        requested_date = "the requested date"
    doctor_name = patient_details.get("doctor_name", "[Doctor's Name]")
    dob = patient_details.get("dob", "[Date of Birth]")
    patient_name = f"{patient_details.get('first_name', '[First Name]')} {patient_details.get('last_name', '[Last Name]')}"
    last_appointment = patient_details.get("last_appointment", "[Last Appointment]")
    next_appointment = patient_details.get("next_appointment", "[Next Appointment]")
    medical_condition = patient_details.get("medical_condition", "[Medical Condition]")
    medication_regimen = patient_details.get("medication_regimen", "[Medication Regimen]")


    # Customize the prompt with patient details
    system_prompt = f"""
You are an AI assistant designed to handle health-related inquiries from patients. You will be given a patient’s message, and based on its content, you should respond appropriately. Here are the instructions on how to respond to various types of messages. Ignore any message that is not health-related or does not fall into one of the categories below.

Categories and Responses:
1. **Appointment-related inquiries**:
- If the patient requests for a new appointment, respond with:
    - **“Your new appointment date is {next_appointment}.”**
   - If the patient requests to reschedule an appointment, respond with:
     - **“I will convey your request to {doctor_name}.”**
   - Also return the following text:
     - **“Patient {patient_name} is requesting an appointment change from {last_appointment} to {requested_date}.”**
   - Example Message: "Can we reschedule the appointment to next Friday at 3 PM?"

2. **Medication-related inquiries**:
   - If the patient inquires about their medication regimen, dosage, or schedule, generate an informative response reminding them to follow the prescribed regimen: **"{medication_regimen}"**, and suggesting consulting with the doctor for any adjustments.
   - Example Message: "Is it okay if I take my medication at a different time?"

3. **General health-related inquiries**:
   - If the patient asks about general health or lifestyle advice, generate a supportive response that offers general health guidance and encourages them to continue seeking advice on their treatment, medication, or lifestyle improvements.
   - Example Message: "Do you have any recommendations for improving my sleep?"

4. **Patient's own medical details**:
   - If the patient inquires about their medical condition or treatment plan, provide the following details: **"{medical_condition}"**, along with any relevant appointments or regimen information. Format the response to make it easily understandable.
   - Example Message: "Can you tell me about my treatment plan?"

5. **Sensitive, irrelevant, or controversial messages**:
   - If the message does not fall into any of the above categories or contains sensitive, unrelated, or controversial content, respond with:
     - **“I'm here to assist with health-related inquiries. For other topics, please consult the appropriate resources.”**

**Message**: "{user_message}"

**Expected Output**: Generate only the response for the user, based on the instructions above in JSON format.
    """
    print('model_name here in function:', model_name)
    # response = LLMOpenAI(OPENAI_API_KEY, model_name).generate_content(system_prompt, user_message) # OpenAI
    response = GeminiChat(OPENAI_API_KEY, model_name).generate_content(system_prompt) # Gemini
    print('response:', response)
    print('res type', type(response))

    try:
        if isinstance(response, dict):
            # Accessing response structure safely
            response_text = response['response']#[0]['content']['parts'][0]['text']
            return {'response': response_text.strip()}
        else:
            raise ValueError("Unexpected response structure")
    except (KeyError, IndexError, ValueError) as e:
        print("Error in extracting response text:", e)
        return {"response": "I'm here to assist with health-related inquiries."}

    # try:
    #     # Parse response to ensure it is JSON formatted
    #     entities_json = json.dumps(response)  # Convert to JSON string if necessary
    #     return entities_json
    # except Exception as e:
    #     print("Error in extract_entities:", e)
    #     return "{}"  # Return an empty JSON object if parsing fails
    # return response  # This will be a JSON-formatted string from the LLM

# def store_in_neo4j(entities_json):
#     # entities = json.loads(entities_json)
#     if not entities_json.strip():
#         print("Empty JSON received in store_in_neo4j")
#         return

#     try:
#         entities = json.loads(entities_json)
#     except json.JSONDecodeError as e:
#         print("JSON decode error:", e)
#         return  # Exit if JSON is invalid
#     with driver.session() as session:
#         # Create patient node if it doesn't exist
#         session.run("MERGE (p:Patient {name: 'John Doe'})")

#         # Add medication, frequency, medical_condition nodes/relationships if they exist
#         if entities.get("medication"):
#             session.run(
#                 """
#                 MERGE (m:Medication {name: $medication})
#                 MERGE (p:Patient {name: 'John Doe'})
#                 MERGE (p)-[:TAKES {frequency: $frequency}]->(m)
#                 """,
#                 medication=entities["medication"],
#                 frequency=entities.get("frequency")
#             )

#         if entities.get("medical_condition"):
#             session.run(
#                 """
#                 MERGE (c:Condition {name: $condition})
#                 MERGE (p:Patient {name: 'John Doe'})
#                 MERGE (p)-[:SUFFERS_FROM]->(c)
#                 """,
#                 condition=entities["medical_condition"]
#             )

#         if entities.get("appointment_time"):
#             session.run(
#                 """
#                 MERGE (a:Appointment {date: $appointment_time})
#                 MERGE (p:Patient {name: 'John Doe'})
#                 MERGE (p)-[:HAS_APPOINTMENT]->(a)
#                 """,
#                 appointment_time=entities["appointment_time"]
#             )

# # def process_user_message(user_message):
# #     # Step 1: Extract entities using the LLM
#     entities_json = extract_entities(user_message)
    
#     # Step 2: Store entities in Neo4j
#     store_in_neo4j(entities_json)
