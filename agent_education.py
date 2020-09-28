import json
import os
import logging
import dialogflow_v2
from dotenv import load_dotenv
import argparse


logger = logging.getLogger('agent_education')


def parse_arguments():
    parser = argparse.ArgumentParser(description='DialogFlow agent education')
    parser.add_argument('training_file_path', type=str,
        help='path to file with training phrases and intents to agent education')
    parser.add_argument('--debug', action='store_true',
        help='set DEBUG level of logger')
    return parser.parse_args()


def read_json_file(file_path):
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


def convert_dict_to_intent(input_tuple):
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


def load_intents_from_file_to_agent(project_id, file_path):
    intent_decriptions = read_json_file(file_path)
    intents = [convert_dict_to_intent(item) 
        for item in intent_decriptions.items()]
    logger.debug(intents[0])
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(project_id)
    for intent in intents:
        response = client.create_intent(parent, intent)


def train_agent(project_id):
    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(project_id)
    response = client.train_agent(parent)


def main():
    load_dotenv()
    args = parse_arguments()
    logging.basicConfig(format='%(asctime)s - %(levelname)s - '
        '%(message)s', datefmt='%m/%d/%Y %H:%M ', level=logging.ERROR)
    if args.debug:
        logger.setLevel(logging.DEBUG)      
    project_id = os.getenv("PROGECT_ID")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getenv("GOOGLE_CREDENTIALS")
    load_intents_from_file_to_agent(project_id, args.training_file_path)
    logger.info('Intents and training phrases are loaded to agent')
    train_agent(project_id)
    logger.info('Start agent training')


if __name__=='__main__':
    main()