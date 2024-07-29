import os
from groq import Groq
from dotenv import load_dotenv
from app import *

load_dotenv()

# Ensure the API key is set
groq_api_key = os.getenv('GROQ_APIKEY2')
if not groq_api_key:
    raise ValueError("API key is not set. Please set the GROQ_API_KEY environment variable.")

# Define a prompt template
prompt_template ="""
You are a tutor. Your task is to guide user students through {selected_topic} and {selected_prompt} help users in the learning process step by step of students' concerns, problems, and subjects, you should instruct the AI to act as a tutor, focusing on understanding the student’s needs and delivering personalized, step-by-step instructions, like understanding the student’s needs, breaking down the subject, providing step-by-step instructions, addressing questions and concerns, assessing understanding, and adapting your teaching style. Go step by step and keep the response short and easy to understand for the user. The response should be a maximum of 70 words.
User: {user_input}
AI: 
"""

def generate_response(selected_topic, selected_prompt, user_input):  
    client = Groq(api_key=groq_api_key)

    # Format the prompt with the user input
    formatted_prompt = prompt_template.format(selected_topic=selected_topic, selected_prompt=selected_prompt, user_input=user_input)

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": formatted_prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )  

    response = ""

    for chunk in completion:
        response += (chunk.choices[0].delta.content or "")
    return response
