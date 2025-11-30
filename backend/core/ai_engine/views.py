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

        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            # Mock response for development without API key
            return Response({
                'title': f"Generated: {prompt[:20]}...",
                'description': f"AI generated component based on: {prompt}",
                'code_content': {
                    'html': '<div class="p-4 bg-blue-500 text-white rounded">AI Generated Component</div>',
                    'css': '',
                    'js': 'console.log("AI Component Loaded");'
                }
            })

        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert frontend developer. Generate a Svelte component based on the user prompt. Return JSON with keys: title, description, code_content (object with html, css, js keys). The html should be Svelte syntax."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            
            import json
            content = json.loads(response.choices[0].message.content)
            return Response(content)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
