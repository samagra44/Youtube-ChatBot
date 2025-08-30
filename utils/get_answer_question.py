from langchain_openai import ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from config.configuratiosn.credentials import HUGGINGFACEHUB_API_TOKEN, OPENAI_API_KEY
from langchain_core.prompts import ChatPromptTemplate
from loggers.logger import logger
import os

os.environ['HUGGINGFACEHUB_API_TOKEN'] = HUGGINGFACEHUB_API_TOKEN
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

def answer_question(question, chat_history):
    logger.info(f"Inside answer_question() Method")
    global global_vector_db
    if global_vector_db is None:
        return "Please Provide the Youtube URL.", chat_history
    
    try:
        llm = ChatOpenAI()
        retriever = global_vector_db.as_retriever(search_kwargs={"k": 5})
        system_prompt = (
            "You are a video assistant tasked with answering questions based on the provided Youtube video context. "
            "Use the given context given by the video author to provide accurate, concise answers in three sentences. "
            "If the context does not contain the answer, say you are not sure "
            "Context: {context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        chain = create_retrieval_chain(retriever, question_answer_chain)
        response = chain.invoke({"input": question})

        if "answer" not in response:
            raise ValueError("response does not an 'answer' key")
        
        chat_history.append((question, response['answer']))
        return response['answer'], chat_history
    except Exception as e:
        logger.error(f"Something went wrong in answer_question() Method: {e}")
        error_message = f"Error: {str(e)}"
        chat_history.append((question, error_message))
        return error_message, chat_history