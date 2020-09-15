import json
import os
import logging
import dialogflow_v2
from dotenv import load_dotenv


def read_json_file(file_path, logger):
    if not os.path.exists(file_path):
        logger.error(f"File doesn't exist: {file_path}")
        return
    with open(file_path, 'r') as file_obj:
        content = json.load(file_obj)
    logger.debug(f"Read file content, data length is {len(content)}")
    logger.debug(f"Content element is {type(content)}")  
    return content


def get_formatted_training_phrase(training_phrase):
    formatted_training_phrase = {
        "parts": [{"text": training_phrase}]
    }
    return formatted_training_phrase


def convert_dict_to_intent(input_tuple, logger):
    intent_name, intent_content = input_tuple
    intent = {
        "display_name": intent_name,
        "messages": [{
            "text": {
                "text": [intent_content["answer"]]
            }
        }],
        "training_phrases": [
            get_formatted_training_phrase(answer) 
                for answer in intent_content["questions"]
        ]
    }
    return intent


def create_intents_from_file(project_id, file_path, logger):
    intent_decriptions = read_json_file(file_path, logger)
    intents = [convert_dict_to_intent(item, logger) 
        for item in intent_decriptions.items()]
    logger.debug(intents[0])
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(project_id)
    for intent in intents:
        response = client.create_intent(parent, intent)


def train_agent(project_id, logger):
    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(project_id)
    response = client.train_agent(parent)


def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
        '%(message)s', level=logging.DEBUG)
    logger = logging.getLogger('chatbot3_agent_education')
    training_file_path = "TrainingPhrases.json"
    project_id = os.getenv("PROGECT_ID")
    # create_intents_from_file(project_id, training_file_path, logger)  
    train_agent(project_id, logger)

if __name__=='__main__':
    main()