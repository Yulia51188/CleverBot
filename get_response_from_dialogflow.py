import logging
from functools import partial
import dialogflow_v2 as dialogflow


def detect_intent_texts(project_id, session_id, texts, language_code, logger):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        logger.debug('=' * 20)
        logger.debug('Query text: {}'.format(response.query_result.query_text))
        logger.debug('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        logger.debug('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text)) 
        fulfillment_text = response.query_result.fulfillment_text
        return fulfillment_text