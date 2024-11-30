from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from dotenv import load_dotenv
import os
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer
from llama_index.core.tools import QueryEngineTool
from llama_index.core import PromptTemplate
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.query_engine import TransformQueryEngine

load_dotenv()

def getEngine():

    new_summary_tmpl_str = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "anwer in detail and give all the information.\n"
        "Give the response in markdown format.\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    new_summary_tmpl = PromptTemplate(new_summary_tmpl_str)

    template = (
        "System: You are an AI assistant named Alex for course CSE 512 Distribute database system at Arizona State University. You have information about ssignments of the course.\n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Human: {query_str}\n"
        "AI: "
    )
    qa_template = PromptTemplate(template)

    response_synthesizer = get_response_synthesizer( text_qa_template = qa_template, summary_template= new_summary_tmpl, 
                                                    streaming = True
                                                    )

    vector_store = ElasticsearchStore(
        es_url="http://localhost:9200",
        index_name="cse512_rag",
    )


    index = VectorStoreIndex.from_vector_store(vector_store)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

    vector_store_query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer
    )

    hyde = HyDEQueryTransform(include_original=True)
    hyde_query_engine = TransformQueryEngine(vector_store_query_engine, hyde)

    return hyde_query_engine, vector_store

