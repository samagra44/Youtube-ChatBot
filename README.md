# Youtube Video Q&A

This repository contains a Python application that allows you to ask questions about a YouTube video and receive concise answers based on the video's content. The application uses the Langchain library for text processing, Hugging Face for embeddings, and OpenAI for question answering.

## Table of Contents
1. **Installation**
2. **Environment Setup**
3. **Running the Application**
4. **Usage**
5. **Acknowledgements**

## Installation

To install the required dependencies, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Environment Setup

1. Create a `.env` file in the root directory of the project and add the following environment variables:

```
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
OPENAI_API_KEY=your_openai_api_key
```

Replace `your_huggingface_api_token` and `your_openai_api_key` with your actual API keys.

2. Load the environment variables in your Python script:

```python
import os
load_dotenv()
```

## Running the Application

Run the following command in your terminal to run the application:

```bash
python app.py
```

## Usage

1. Enter a YouTube video URL in the provided textbox.
2. Click the "Submit URL" button to process the video and make it available for questions.
3. Once the video is processed, you can ask questions about the video in the chat interface.
4. Click the "Ask Question" button to receive an answer based on the video's content.
5. You can clear the chat history by clicking the "Clear Chat" button.

## Acknowledgements

This project uses the following libraries:

- [Gradio](https://www.gradio.app/)
- [Langchain](https://github.com/hwchase17/langchain)
- [Langchain Hugging Face](https://github.com/hwchase17/langchain-huggingface)
- [Langchain OpenAI](https://github.com/hwchase17/langchain-openai)
- [Langchain Core](https://github.com/hwchase17/langchain-core)
- [Langchain Community](https://github.com/hwchase17/langchain-community)
- [Hugging Face](https://huggingface.co/)
- [OpenAI](https://openai.com/)
- [Dotenv](https://github.com/theskumar/dotenv)
