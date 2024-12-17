import gradio as gr
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.youtube import YoutubeLoader
import os

os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'your_huggingface_api_token'
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'

def process_youtube_url(youtube_url):
    loader = YoutubeLoader.from_youtube_url(youtube_url=youtube_url, add_video_info=False)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=256,
        separators=['\n\n', '\n', '']
    )

    split_docs = splitter.split_documents(documents=documents)
    embeddings = HuggingFaceEndpointEmbeddings()
    db = FAISS.from_documents(split_docs, embeddings)
    return db

def submit_url(youtube_url):
    global global_vector_db
    try:
        global_vector_db = process_youtube_url(youtube_url=youtube_url)
        default_question = "Summarize this video"
        chat_history = []
        summary, _ = answer_question(default_question, chat_history)
        status_message = "Video loaded successfuly! ✅ You can ask questions now"
    except Exception as e:
        status_message = f"Failed to get the video because of: {e}"
        summary = ""
    
    return status_message, summary

def answer_question(question, chat_history):
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
        error_message = f"Error: {str(e)}"
        chat_history.append((question, error_message))
        return error_message, chat_history


def ask_question(question, chat_history):
    response, updated_chat_history = answer_question(question=question, chat_history=chat_history)
    return updated_chat_history, updated_chat_history


def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("<h1 style='text-align: center'; color: #4A90E2;>Youtube Video Q&A</h1>")
        gr.Markdown("<p style='text-align: center;'>Enter a Youtbe Video URL</p>")
        with gr.Row():
            with gr.Column(scale=1):
                youtube_url = gr.Textbox(label="Youtube Video URL", placeholder="Enter the Youtube video URL here...", lines=1)
                submit_btn = gr.Button("Submit URL", variant="primary")
                status_info = gr.Textbox(label="Status Info", placeholder="Indexing status will appear here...", interactive=False, lines=2)
                summary_box = gr.Textbox(label="Video Summary", placeholder="Summary will appear here...", interactive=False, lines=6)
                submit_btn.click(fn=submit_url, inputs=youtube_url, outputs=[status_info, summary_box])

            with gr.Column(scale=1):
                    chat_history = gr.Chatbot()
                    question = gr.Textbox(label="Your Question", placeholder="Ask a question about the video...", lines=1)
                    ask_btn = gr.Button("Ask Question", variant="primary")
                    clear_btn = gr.Button("Clear Chat", variant="secondary")
                    state = gr.State([])
                    ask_btn.click(fn=ask_question, inputs=[question, state], outputs=[chat_history, state])
                    clear_btn.click(fn=lambda: ([], []), inputs=[], outputs=[chat_history, state])
        gr.Markdown("<footer style='text-align: center; margin-top: 20px'>Made by - Samagra Shrivastava</footer>")
    return demo

if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch()