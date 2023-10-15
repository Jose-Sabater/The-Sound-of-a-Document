"""Parse the country_information.json file and create a ChromaDB collection with the data."""
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()
import os
import json

from sentence_transformers import SentenceTransformer


hf_api_key = os.getenv("HF_API_KEY")
hf_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    hf_api_key, model_name="BAAI/bge-base-en-v1.5"
)
chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
collection = chroma_client.get_or_create_collection(
    "country_information", embedding_function=hf_ef
)

# load data
with open("./data/countries/country_information.json", "r") as f:
    countries_information = json.load(f)


# Divide in chunks
def split_into_chunks(text, chunk_size=300, min_last_chunk_size=100):
    words = text.split()
    chunks = []
    chunk = []
    i = 0

    while i < len(words):
        word = words[i]
        if len(chunk) + len(word.split()) <= chunk_size:
            chunk.extend(word.split())
            i += 1
        else:
            if word.endswith("."):
                chunk.extend(word.split())
                chunks.append(chunk)
                chunk = []
                i += 1
            else:
                # Look for a period in the next few words to find a better breaking point
                temp_chunk = chunk.copy()
                lookahead_pos = i
                found_period = False
                while lookahead_pos < len(words):
                    next_word = words[lookahead_pos]
                    temp_chunk.extend(next_word.split())
                    lookahead_pos += 1
                    if next_word.endswith("."):
                        found_period = True
                        chunk = temp_chunk
                        chunks.append(chunk)
                        chunk = []
                        i = lookahead_pos  # Update main loop's position
                        break

                if not found_period:
                    chunks.append(chunk)
                    chunk = [word]
                    i += 1

    if chunk:
        if len(chunk) < min_last_chunk_size and chunks:
            chunks[-1].extend(chunk)
        else:
            chunks.append(chunk)

    return [" ".join(chunk) for chunk in chunks]


def process_json(data):
    documents = []
    metadatas = []
    ids = []

    id_counter = 1

    for country, details in data.items():
        for source in ["content", "summary"]:
            text = details[source]
            chunks = split_into_chunks(text)

            for idx, chunk in enumerate(chunks):
                documents.append(chunk)
                last_word_prev_chunk = (
                    "None" if idx == 0 else chunks[idx - 1].split()[-1]
                )

                if idx < len(chunks) - 1:
                    next_chunk_first_words = " ".join(chunks[idx + 1].split()[:3])
                else:
                    next_chunk_first_words = "None"

                metadata = {
                    "country": country,
                    "paragraph": idx + 1,
                    "last_word": chunk.split()[-1],
                    "next_words": next_chunk_first_words,
                    "last_word_prev_chunk": last_word_prev_chunk,
                    "source": source,
                }
                metadatas.append(metadata)
                ids.append(f"{id_counter}")
                id_counter += 1

    return documents, metadatas, ids


documents, metadatas, ids = process_json(countries_information)


sentences_1 = documents
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
embeddings_1 = model.encode(sentences_1, normalize_embeddings=True)
embeddings = embeddings_1.tolist()
collection.add(embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids)
collection.query(query_texts=["What is the capital of France?"], n_results=10)
