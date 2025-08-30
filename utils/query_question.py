from .get_answer_question import answer_question
from loggers.logger import logger

def ask_question(question, chat_history):
    try:
        logger.info(f"Inside ask_question() Method")
        updated_chat_history = answer_question(question=question, chat_history=chat_history)
        return updated_chat_history, updated_chat_history
    except Exception as e:
        logger.error(f"Something went wrong in ask_question() Method: {e}")