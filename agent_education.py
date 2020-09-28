import json
import os
import logging
import dialogflow_v2
from dotenv import load_dotenv
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='DialogFlow agent education')
    parser.add_argument('training_file_path', type=str,
        help='path to file with training phrases and intents to agent education')
    parser.add_argument('--debug', action='store_true',
        help='set DEBUG level of logger')
    return parser.parse_args()


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


def load_intents_from_file_to_agent(project_id, file_path, logger):
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
    args = parse_arguments()
    logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - '
        '%(message)s', level=logging.DEBUG)
    logger = logging.getLogger('dialogflow_agent_education')
    project_id = os.getenv("PROGECT_ID")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getenv("GOOGLE_CREDENTIALS")
    load_intents_from_file_to_agent(project_id, args.training_file_path, logger)
    train_agent(project_id, logger)


if __name__=='__main__':
    main()