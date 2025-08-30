from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain_community.document_loaders.youtube import YoutubeLoader
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from loggers.logger import logger

def process_youtube_url(youtube_url):
    logger.info(f"Inside process_youtube_url() Method")
    try:
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
    
    except Exception as error:
       logger.error(f"Something went wrong in process_youtube_url() Method: {error}")