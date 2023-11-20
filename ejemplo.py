import google.generativeai as palm
from googletrans import Translator
import json

translator = Translator()


while True:

    # Customer request, context and specefications for the ai

    context_prompt = "Create a list of task, focused to"
    prompt = input('\nDescribe detalladamente el objetivo que quieres cumplir: ')
    specifications = 'Only return a JSON and make sure that every key and value have their respective double quotation marks.'

    if prompt:
        if prompt == 'exit':
            break
        else:
            # API's key
            palm.configure(api_key='AIzaSyB-aTCaz7CAQ3HbrTUuoFP-wZ-M6lvWJlg')

            # Translation of the prompt for the ai
            language = translator.detect(prompt).lang
            text_tranlated = translator.translate(prompt, src=language, dest='en').text

            # Chatting with the ai, sending the context, the prompt, the specifications, the temperature and the model
            response = palm.chat(model='models/chat-bison-001',
                                 context="Return JSON with those keys: name, description, est_time_min, priority_level. Only follow this example, never change the structure.",
                                 messages=(f"{context_prompt}: {text_tranlated}. And {specifications}", context_prompt ,text_tranlated, specifications),
                                 temperature=0)
            

            # validating the response, translating it and converting it to JSON
            response_ai = response.last
            index = response_ai.find('json')
            if index :
                response_ai = (response.last[index+5:-4])

                if not response_ai.find('['):
                    language = translator.detect(response_ai).lang
                    tasks = json.loads(response_ai)
                    tasks_modified = [{**task, 'name': translator.translate(task['name'], src=language, dest="es").text, 'description': translator.translate(task['description'], src=language, dest="es").text} for task in tasks]
                    tasks_modified = json.dumps(tasks_modified)
                    print(tasks_modified)

                else:
                    language = translator.detect(response_ai).lang
                    task = json.loads(response_ai)
                    task["name"] = translator.translate(task["name"], src=language, dest="es").text
                    task["description"] = translator.translate(task["description"], src=language, dest="es").text
                    task = json.dumps(task)
                    print(task)

    else:
        print('Por favor ingrese una pregunta valida.')
