from .database.models.user_info import EmailPasswordUser, ThirdPartyUser
from supertokens_backend.database.db_source import SessionLocal
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from supertokens_python.recipe.session.framework.django.syncio import verify_session
from django.http import JsonResponse
from supertokens_backend.database.queries.save_text_queries import SaveUserTextQueries
import requests
from supertokens_backend.openai_helper import OpenAIHelper
import json
import os


class getUserDetailsAPI(APIView):
    
    @method_decorator(verify_session())
    def get(self, request, method=['GET']):
        try:
            session = request.supertokens
            current_user_id = session.get_user_id()
            db_session = SessionLocal()
            try:
                
                user = db_session.query(EmailPasswordUser).filter(EmailPasswordUser.user_id == current_user_id).first()
                
                if not user:
                    user = db_session.query(ThirdPartyUser).filter(ThirdPartyUser.user_id == current_user_id).first()

                if user:
                    email = user.email
                else:
                    return JsonResponse({"status": False, "message": "User not found"})

            finally:
                db_session.close()

            return JsonResponse({
                "status": "success",
                "data": {
                    "user_id": current_user_id,
                    "email": email
                }
            })
        except Exception as e:
            db_session.close()
            return JsonResponse({
                "status": False,
                "message": f"Error: {str(e)}"
            })
        
class SaveUserTextAPI(APIView):

    @method_decorator(verify_session())
    def post(self, request):
        try:
            session = request.supertokens
            current_user_id = session.get_user_id()
            text = request.data.get('text')
            isSaved = SaveUserTextQueries.insert_text(current_user_id,text)
            if isSaved:
                return JsonResponse({"status": True,"message":"Your Text Saved"})
            return JsonResponse({"status": False,"message": "Something went wrong!"})
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error: {str(e)}"
            })
        
    @method_decorator(verify_session())
    def get(self, request):
        try:
            session = request.supertokens
            current_user_id = session.get_user_id()
            is_data_received, data, day_count, week_count = SaveUserTextQueries.get_saved_texts(current_user_id)
            if is_data_received:
                # Properly structure the dictionary keys with string literals
                return JsonResponse({
                    "status": True,
                    "data": data,  # This sends the list of data as 'data' in the JSON.
                    "day_count": day_count,
                    "week_count": week_count
                })
            else:
                return JsonResponse({"status": False, "message": "Data not retrieved"})
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Error: {str(e)}"
            })
        

class TextModifier(APIView):
    def post(self, request):
        text = request.data.get('text')
        option = request.data.get('option')

        if not text or not option:
            return JsonResponse({'status': 'error', 'message': 'Missing text or option'}, status=400)

        prompt = self.create_prompt(text, option)

        openai_key = os.getenv('OPENAI_AUTH_KEY_NEW')
        openai_response = OpenAIHelper.generate_text(openai_key, prompt)

        # Process the API response
        if openai_response:
            return JsonResponse({'status': 'success', 'data': openai_response})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to generate response'}, status=400)

    def create_prompt(self, text, option):
       

        if option == 'correct':
            prompt = f"Original text: {text}\n"
            prompt += "Instructions: Correct the grammar and spelling errors in the following text. "
            prompt += "If you don't find any errors, just return the text."
            return prompt


        elif option == 'elaborate':
            max_length = len(text.split()) + 5
            prompt = (f"Original text: '{text}'\n"
                    f"Instructions: Elaborate on the above text without exceeding {max_length} total words.")
            return prompt
        
        elif option == 'shorten':
            if len(text.split()) == 1:
                prompt = f"Original word: '{text}'\n"
                prompt += "Instructions: Provide a shorter word or abbreviation that represents the original word."
            else:
                prompt = f"Original text: '{text}'\n"
                prompt += "Instructions: Summarize the following text in fewer words while retaining the key information."
            return prompt

        elif option == 'rewrite':
            prompt = f"Original text: '{text}'\n"
            prompt += "Instructions: Rewrite the following text to improve clarity and readability while maintaining the same meaning."
            return prompt
        
        else:
            return "No valid option selected."


class RephraseTextView(APIView):
    def post(self, request):
        original_text = request.data.get('text', '')
        if not original_text:
            return JsonResponse({'status': 'failure', 'message': 'No text provided'}, status=400)

        new_prompt = (f"Please rephrase the following text to correct grammatical mistakes and improve sentence structure. "
                  f"Provide the rephrased versions as three separate entries, each in its own array, within a larger array. "
                  f"Each version should retain the same meaning as the original: \n\n"
                  f"'{original_text}'"
                  )

        openai_key = os.getenv('OPENAI_AUTH_KEY_NEW')
        rephrased_text = OpenAIHelper.rephrase(openai_key, new_prompt)

        if rephrased_text:
            return JsonResponse({'status': 'success', 'data': rephrased_text})
        else:
            return JsonResponse({'status': 'failure', 'message': 'Response generation failed'}, status=400)

class ValidateTextView(APIView):
    def post(self, request):
        original_text = request.data.get('text', '')
        print(original_text)
        if not original_text:
            return JsonResponse({'status': 'failure', 'message': 'No text provided'}, status=400)

        # Define the new prompt for analyzing the text
        new_prompt = (
            "Process the following text by splitting it based on newlines. "
            "For each sentence, identify any grammatical errors. If an error is found, correct the sentence, "
            "note the grammatical rule that was violated, and provide this information. "
            "Additionally, for each error, provide an example demonstrating the incorrect and correct usage. "
            "Output the data in a JSON format, where each entry contains the 'original' sentence, "
            "'corrected' sentence, 'rule' violated, and an 'example' object with 'incorrect' and 'correct' fields. "
            "Only include sentences that have errors."
            f"Text to analyze:\\n{original_text}"
        )



        openai_key = os.getenv("OPENAI_AUTH_KEY_NEW")
        print(openai_key,"openai")
        analysis = OpenAIHelper.analyze_text(openai_key, new_prompt)

        if analysis:
            # Convert string representation of list of dicts to actual JSON
            try:
                analysis_json = json.loads(analysis)
                return JsonResponse({'status': 'success', 'data': {'analysis': analysis_json}})
            except json.JSONDecodeError:
                return JsonResponse({'status': 'failure', 'message': 'Error in parsing analysis result'}, status=500)
        else:
            return JsonResponse({'status': 'failure', 'message': 'Error analyzing text'}, status=500)







class GrammarCheckView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        url = "https://api.languagetool.org/v2/check"
        data = {
            'text': text,
            'language': 'en-US'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=data, headers=headers)
        
        if response.status_code == 200:
            results = response.json()
            errors = [{'message': match['message'], 'offset': match['offset'], 'length': match['length']} for match in results.get('matches', [])]
            return JsonResponse({'correctedText': text, 'errors': errors})
        else:
            return JsonResponse({'error': 'Failed to process the text'})