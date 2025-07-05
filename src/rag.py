from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms import Ollama
from llama_index.embeddings.fastembed import FastEmbedEmbedding
import os
from typing import List, Optional
import config

class ShopManualRAG:
    def __init__(self):
        # Initialize Ollama
        self.llm = Ollama(
            model=config.MODEL_NAME,
            base_url=config.OLLAMA_BASE_URL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
        )
        
        # Initialize embeddings using fastembed to avoid heavy torch dependency
        self.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
        
        # Create service context
        self.service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model=self.embed_model,
        )
        
        self.index = None
        if os.path.exists(config.INDEX_PATH):
            self.load_index()
    
    def index_documents(self) -> None:
        """Index all documents in the docs directory."""
        documents = SimpleDirectoryReader(config.DOCS_DIR).load_data()
        self.index = VectorStoreIndex.from_documents(
            documents,
            service_context=self.service_context,
        )
        self.index.storage_context.persist(persist_dir=config.DATA_DIR)
    
    def load_index(self) -> None:
        """Load the existing index from disk."""
        if os.path.exists(config.INDEX_PATH):
            storage_context = StorageContext.from_defaults(persist_dir=config.DATA_DIR)
            self.index = load_index_from_storage(storage_context)
    
    def query(self, query_text: str) -> str:
        """Query the indexed documents."""
        if not self.index:
            raise ValueError("No index available. Please index documents first.")
        
        query_engine = self.index.as_query_engine(
            response_mode=config.RESPONSE_MODE
        )
        response = query_engine.query(query_text)
        return str(response)
    
    def get_relevant_documents(self, query_text: str, num_docs: int = 3) -> List[str]:
        """Get the most relevant document snippets for a query."""
        if not self.index:
            raise ValueError("No index available. Please index documents first.")
        
        retriever = self.index.as_retriever(similarity_top_k=num_docs)
        nodes = retriever.retrieve(query_text)
        return [node.node.text for node in nodes] 