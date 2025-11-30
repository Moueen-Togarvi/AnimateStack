from celery import shared_task
from openai import OpenAI
import os
import json

@shared_task
def generate_component_task(prompt, user_id):
    # This task would handle the AI generation in the background
    # and then notify the user via Channels (WebSocket)
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {'error': 'No API Key'}

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert frontend developer. Generate a Svelte component..."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        content = json.loads(response.choices[0].message.content)
        
        # Here we would:
        # 1. Save the component to DB
        # 2. Send a WebSocket message to the user saying "Generation Complete"
        
        return content
    except Exception as e:
        return {'error': str(e)}
