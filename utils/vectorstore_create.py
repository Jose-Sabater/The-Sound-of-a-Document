from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.node_parser import SimpleNodeParser
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import download_loader
import chromadb
import json
from config import secrets
import os

os.environ["OPENAI_API_KEY"] = secrets["OPENAI_API_KEY"]

chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
collection = chroma_client.get_or_create_collection("country_information")

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model,
                                            chunk_size=300,
                                            node_parser=SimpleNodeParser.from_defaults())

# Load data
with open("./data/country_information.json", "r") as f:
    data =  json.load(f)
JsonDataReader = download_loader("JsonDataReader")
loader = JsonDataReader()
documents = loader.load_data(data)


index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, service_context=service_context
)

# Query Data from the persisted index
query_engine = index.as_query_engine()
response = query_engine.query("What is the capital of spain?")
