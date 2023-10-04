from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles import finders
from django.views.generic import View
from django.templatetags.static import static
import json

class ScriptView(View):
    def get(self, request, *args, **kwargs):
        script_path = finders.find('chatbot/script.js')
        if script_path:
            with open(script_path, 'r') as script_file:
                script_content = script_file.read()
            return HttpResponse(script_content, content_type='text/javascript')
        else:
            return HttpResponse('Script not found', status=404)

user_responses = {}

dosha_weights = {
    "Vata": {
        1: 2,  
        2: 2,  
        3: 2,  
        4: 2,  
        5: 2,  
    },
    "Pitta": {
        6: 2,  
        7: 2,  
        8: 2,  
        9: 2,  
        10: 2,  
    },
    "Kapha": {
        11: 2,
        12: 2,
        13: 2,
        14: 2,
        15: 2,
    }
}

# Load questionnaire data outside of the function
with open('chatbot/questionnaire.json', 'r') as file:
    questionnaire = json.load(file)

def index(request, question_id=1):
    question = questionnaire['questions'][question_id - 1]['text']

    context = {
        'question_id': question_id,
        'question': question,
    }
    return render(request, 'chatbot/index.html', context)

def submit(request):
    user_response = request.POST['response']
    question_id = int(request.POST['question_id'])

    user_responses[question_id] = user_response

    if question_id < len(questionnaire['questions']):
        next_question_id = question_id + 1
        next_question = questionnaire['questions'][next_question_id - 1]['text']
        context = {
            'question_id': next_question_id,
            'question': next_question,
        }
        return render(request, 'chatbot/index.html', context)
    else:
        prakruti_type = assess_prakruti(user_responses)
        feedback = provide_feedback(prakruti_type)
        user_responses.clear()

        response_data = {
            'response': f"Your dominant dosha is {prakruti_type}. {feedback}"
        }
        return JsonResponse(response_data)

def assess_prakruti(user_responses):
    dosha_scores = {"Vata": 0, "Pitta": 0, "Kapha": 0}

    for dosha, weights in dosha_weights.items():
        for question_id, weight in weights.items():
            if question_id in user_responses:
                user_response = user_responses[question_id].lower()
                
                if dosha in user_response:
                    dosha_scores[dosha] += weight
    
    dominant_dosha = max(dosha_scores, key=dosha_scores.get)

    return dominant_dosha

def provide_feedback(prakruti_type):
    feedback_messages = {
        "Vata": "Your dominant dosha is Vata. Vata-dominant individuals may have a slender frame, dry skin, and may feel cold easily.",
        "Pitta": "Your dominant dosha is Pitta. Pitta-dominant individuals may have a warm body temperature and enjoy spicy or acidic foods.",
        "Kapha": "Your dominant dosha is Kapha. Kapha-dominant individuals may have a stable appetite but may tend to overeat."
    }

    return feedback_messages.get(prakruti_type, "Your Prakruti type is balanced.")
