from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import os
from openai import OpenAI

class GenerateComponentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key or api_key == 'sk-placeholder-key-replace-me':
            # Mock response for development without API key
            return Response({
                'title': f"Generated: {prompt[:20]}...",
                'description': f"AI generated component based on: {prompt}",
                'code_content': {
                    'html': '<div class="p-4 bg-blue-500 text-white rounded">AI Generated Component (Mock)</div>',
                    'css': '',
                    'js': 'console.log("AI Component Loaded");'
                }
            })

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            system_prompt = """
            You are an expert frontend developer. Generate a Svelte component based on the user prompt. 
            Return ONLY a valid JSON object with the following structure:
            {
                "title": "Component Title",
                "description": "Brief description",
                "code_content": {
                    "html": "Svelte HTML/Template code here",
                    "css": "CSS styles here (no <style> tags)",
                    "js": "JavaScript logic here (no <script> tags)"
                }
            }
            Do not include markdown formatting (```json ... ```). Just the raw JSON string.
            """
            
            full_prompt = f"{system_prompt}\n\nUser Prompt: {prompt}"
            
            response = model.generate_content(full_prompt)
            
            import json
            # Clean up potential markdown formatting if Gemini adds it
            content_str = response.text.strip()
            if content_str.startswith('```json'):
                content_str = content_str[7:]
            if content_str.endswith('```'):
                content_str = content_str[:-3]
                
            content = json.loads(content_str)
            return Response(content)

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"AI Generation Error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
