from dotenv import load_dotenv
import os
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv()
documents = SimpleDirectoryReader("../data/").load_data()

vector_store = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="cse512_rag",
    # es_user = 'elastic',
    # es_password = os.getenv("ELASTIC_PASSOWRD"),
    # verify_certs=False
)

pipeline = IngestionPipeline(
    transformations=[
        # SentenceSplitter(chunk_size=512, chunk_overlap = 70),
        SentenceSplitter(),
        OpenAIEmbedding(),
    ],
    vector_store=vector_store,
)
nodes = pipeline.run(documents=documents)

vector_store.close()