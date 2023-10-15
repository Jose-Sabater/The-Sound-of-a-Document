from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.node_parser import SimpleNodeParser
from llama_index.embeddings import HuggingFaceEmbedding
import chromadb
from config import secrets
import os

os.environ["OPENAI_API_KEY"] = secrets["OPENAI_API_KEY"]

chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
collection = chroma_client.get_or_create_collection("country_information")
vector_store = ChromaVectorStore(chroma_collection=collection)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(
    embed_model=embed_model,
    chunk_size=300,
    node_parser=SimpleNodeParser.from_defaults(),
)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    show_progress=True,
    service_context=service_context,
)

query_engine = index.as_query_engine(verbose=True)
response = query_engine.query("What is the capital of spain?")
print(response)

# INFO: Cost on API from the above call
# 08:00
# gpt-3.5-turbo-0613, 1 request
# 2,025 prompt + 7 completion = 2,032 tokens
