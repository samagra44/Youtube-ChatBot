import gradio as gr
from .url_submit import submit_url
from .query_question import ask_question
from loggers.logger import logger

def create_gradio_interface():
    try:
        logger.info(f"Inside create_gradio_interface() Method")
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
    except Exception as e:
         logger.error(f"Something went wrong in create_gradio_interface() Method: {e}")