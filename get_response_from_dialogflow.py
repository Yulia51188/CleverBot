import dialogflow_v2 as dialogflow
import logging

from functools import partial

logger = logging.getLogger('verb_game_bot')

def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)

    logger.debug('Query text: {}'.format(response.query_result.query_text))
    logger.debug('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    logger.debug('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text)) 

    fulfillment_text = response.query_result.fulfillment_text
    is_fallback = response.query_result.intent.is_fallback
    return (fulfillment_text, is_fallback)