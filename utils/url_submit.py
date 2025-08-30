from .process_url import process_youtube_url
from .get_answer_question import answer_question
from loggers.logger import logger

def submit_url(youtube_url):
    logger.info(f"Inside submit_url() Method")
    global global_vector_db
    try:
        global_vector_db = process_youtube_url(youtube_url=youtube_url)
        default_question = "Summarize this video"
        chat_history = []
        summary, _ = answer_question(default_question, chat_history)
        status_message = "Video loaded successfuly! ✅ You can ask questions now"
    except Exception as e:
        logger.error(f"Something went wrong in submit_url() Method: {e}")
        status_message = f"Failed to get the video because of: {e}"
        summary = ""
    
    return status_message, summary