import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")