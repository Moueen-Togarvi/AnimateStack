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
            You are an expert frontend developer specializing in creating "Pro-level", award-winning UI components similar to those found on uiverse.io or aceternity.
            
            Your goal is to generate a Svelte component based on the user prompt.
            
            GUIDELINES:
            1. **Design Quality**: The design MUST be modern, premium, and visually stunning. Use gradients, glassmorphism, subtle shadows, and smooth animations.
            2. **Tech Stack**: Use HTML, CSS (TailwindCSS), and JavaScript.
            3. **Responsiveness**: Ensure the component looks great on all sizes.
            4. **Interactivity**: Add hover effects, transitions, and click animations. Make it feel "alive".
            5. **No Placeholders**: Avoid using placeholder images (like via.placeholder.com) unless absolutely necessary. Use CSS-based graphics or patterns instead.
            6. **Centering**: The component should be designed to look good when centered on the screen.
            
            OUTPUT FORMAT:
            Return ONLY a raw JSON object with the following structure (no markdown code blocks):
            {
                "title": "A creative title for the component",
                "description": "A short description of what it does",
                "code_content": {
                    "html": "The HTML structure (use Tailwind classes)",
                    "css": "Custom CSS if needed (e.g., for keyframe animations not in Tailwind)",
                    "js": "JavaScript logic (if any)"
                }
            }
            """
            
            full_prompt = f"{system_prompt}\n\nUser Prompt: {prompt}"
            
            print(f"Generating for prompt: {prompt}")
            response = model.generate_content(full_prompt)
            
            import json
            content_str = response.text.strip()
            print(f"Raw AI Response: {content_str}")
            
            # Clean up potential markdown formatting
            if content_str.startswith('```json'):
                content_str = content_str[7:]
            elif content_str.startswith('```'):
                content_str = content_str[3:]
            
            if content_str.endswith('```'):
                content_str = content_str[:-3]
            
            content_str = content_str.strip()
                
            try:
                content = json.loads(content_str)
            except json.JSONDecodeError:
                # Fallback: try to find JSON object if there's extra text
                start = content_str.find('{')
                end = content_str.rfind('}') + 1
                if start != -1 and end != -1:
                    content_str = content_str[start:end]
                    content = json.loads(content_str)
                else:
                    raise

            # Validate structure
            if 'code_content' not in content:
                # Attempt to fix structure if AI returned flat keys
                if 'html' in content:
                    content = {
                        'title': content.get('title', 'Generated Component'),
                        'description': content.get('description', 'AI Generated'),
                        'code_content': {
                            'html': content.get('html', ''),
                            'css': content.get('css', ''),
                            'js': content.get('js', '')
                        }
                    }
                else:
                    print("Invalid structure received")

            return Response(content)

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"AI Generation Error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
