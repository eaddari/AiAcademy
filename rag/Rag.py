from dataclasses import dataclass
from langchain_openai import AzureOpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os 
import glob
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI
from langchain.schema import Document
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    HnswConfigDiff,
    OptimizersConfigDiff,
    ScalarQuantization,
    ScalarQuantizationConfig,
    PayloadSchemaType,
    FieldCondition,
    MatchValue,
    MatchText,
    Filter,
    SearchParams,
    PointStruct,
)


load_dotenv()
@dataclass
class Settings:
    # Persistenza FAISS
    persist_dir: str = "faiss_index_example"
    qdrant_url: str = "http://localhost:6333"
    # Text splitting
    chunk_size: int = 700
    chunk_overlap: int = 100
    collection: str = "rag_chunks"
    # Retriever (MMR)
    search_type: str = "mmr"        # "mmr" o "similarity"
    k: int = 4                      # risultati finali
    fetch_k: int = 20               # candidati iniziali (per MMR)
    mmr_lambda: float = 0.3         # 0 = diversificazione massima, 1 = pertinenza massima
    # Embedding
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    key = os.getenv("API_KEY")
    llm_key = os.getenv("API_LLM_KEY")
    azure_llm_endpoint = os.getenv("AZURE_LLM_ENDPOINT")
    #hf_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    # LM Studio (OpenAI-compatible)
    deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
    model_name: str = "gpt-4.1"
    lmstudio_model_env: str = "LMSTUDIO_MODEL"  # nome del modello in LM Studio, via env var
    hf_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

class Rag:

    def __init__(self,settings: Settings):
        # Chunk -> Embedding -> store  
        self.embedder = self.define_embedder(settings)
        #self.embedder = self.define_HugginFacembedder(settings)
        self.llm = self.define_llm(settings)
        client = self.get_qdrant_client(settings)
        #splittare i docs
        chunks = self.split_docs()

        #converte i chunks in una loro rappresentazione vettoriale 
        #self.vec_db = self.define_vector_db(settings,chunks)
        vector_size = 1536
        self.recreate_collection_for_rag(client, settings, vector_size)
        self.upsert_chunks(client, settings, chunks,self.embedder)
        print("Qdrant Configuraziont succeced!")
        #self.retriver = self.make_retriever(settings)

        self.chain = self.build_rag_chain()


    def define_llm(self,settings: Settings):
        llm = AzureChatOpenAI(
            api_version="2024-12-01-preview",
            azure_endpoint=settings.azure_llm_endpoint,
            api_key=settings.llm_key,
            azure_deployment="gpt-4.1",  # Replace with actual deployment
            temperature=0.1,
            max_tokens=1000,  # Optional: control response length
        )
        return llm
    
    def define_embedder(self, settings: Settings):
        embedding = AzureOpenAIEmbeddings(
            api_version="2024-12-01-preview",
            azure_endpoint=settings.azure_endpoint,
            api_key=settings.key,
        )
        return embedding
    def recreate_collection_for_rag(self,client: QdrantClient, settings: Settings, vector_size: int):
        """
        Create or recreate a Qdrant collection optimized for RAG (Retrieval-Augmented Generation).
        
        This function sets up a vector database collection with optimal configuration for
        semantic search, including HNSW indexing, payload indexing, and quantization.
        
        Args:
            client: Qdrant client instance for database operations
            settings: Configuration object containing collection parameters
            vector_size: Dimension of the embedding vectors (e.g., 384 for MiniLM-L6)
            
        Collection Architecture:
        - Vector storage: Dense vectors for semantic similarity search
        - Payload storage: Metadata and text content for retrieval
        - Indexing: HNSW for approximate nearest neighbor search
        - Quantization: Scalar quantization for memory optimization
            
        Distance Metric Selection:
        - Cosine distance: Normalized similarity, good for semantic embeddings
        - Alternatives: Euclidean (L2), Manhattan (L1), Dot product
        - Cosine preferred for normalized embeddings (sentence-transformers)
            
        HNSW Index Configuration:
        - m=32: Average connections per node (higher = better quality, more memory)
        - ef_construct=256: Search depth during construction (higher = better quality, slower build)
        - Trade-offs: Higher values improve recall but increase memory and build time
            
        Optimizer Configuration:
        - default_segment_number=2: Parallel processing segments
        - Benefits: Faster indexing, better resource utilization
        - Considerations: More segments = more memory overhead
            
        Quantization Strategy:
        - Scalar quantization: Reduces vector precision from float32 to int8
        - Memory savings: ~4x reduction in vector storage
        - Quality impact: Minimal impact on search accuracy
        - always_ram=False: Vectors stored on disk, loaded to RAM as needed
            
        Payload Indexing Strategy:
        - Text index: Full-text search capabilities (BM25 scoring)
        - Keyword indices: Fast exact matching and filtering
        - Performance: Significantly faster than unindexed field searches
            
        Collection Lifecycle:
        - recreate_collection: Drops existing collection and creates new one
        - Use case: Development/testing, major schema changes
        - Production: Consider using create_collection + update_collection_info
            
        Performance Considerations:
        - Build time: HNSW construction scales with collection size
        - Memory usage: Vectors loaded to RAM during search
        - Storage: Quantized vectors + payload data
        - Query latency: HNSW provides sub-millisecond search times
            
        Scaling Guidelines:
        - Small collections (<100K vectors): Current settings optimal
        - Medium collections (100K-1M vectors): Increase m to 48-64
        - Large collections (1M+ vectors): Consider multiple collections or sharding
        """
        client.recreate_collection(
            collection_name=settings.collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            hnsw_config=HnswConfigDiff(
                m=32,             # grado medio del grafo HNSW (maggiore = più memoria/qualità)
                ef_construct=256  # ampiezza lista candidati in fase costruzione (qualità/tempo build)
            ),
            optimizers_config=OptimizersConfigDiff(
                default_segment_number=2  # parallelismo/segmentazione iniziale
            ),
            quantization_config=ScalarQuantization(
                scalar=ScalarQuantizationConfig(type="int8", always_ram=False)  # on-disk quantization dei vettori
            ),
        )

        # Indice full-text sul campo 'text' per filtri MatchText
        client.create_payload_index(
            collection_name=settings.collection,
            field_name="text",
            field_schema=PayloadSchemaType.TEXT
        )

        # Indici keyword per filtri esatti / velocità nei filtri
        for key in ["doc_id", "source", "title", "lang"]:
            client.create_payload_index(
                collection_name=settings.collection,
                field_name=key,
                field_schema=PayloadSchemaType.KEYWORD
            )

    def define_HugginFacembedder(self, settings: Settings) -> HuggingFaceEmbeddings:
            """
            Initialize and return a HuggingFace embeddings model instance.
            
            This function creates a sentence transformer model that converts text into
            high-dimensional vector representations for semantic similarity search.
            
            Args:
                settings: Configuration object containing the model name and parameters
                
            Returns:
                HuggingFaceEmbeddings: Configured embedding model instance
                
            Model Loading Behavior:
            - First run: Downloads model from HuggingFace Hub (requires internet)
            - Subsequent runs: Loads from local cache (~/.cache/huggingface/)
            - Model size: 100MB-2GB depending on the selected model
                
            Performance Notes:
            - GPU acceleration: Automatically uses CUDA if available
            - CPU fallback: Falls back to CPU if GPU unavailable
            - Memory usage: Model loaded into RAM/VRAM during inference
                
            Error Handling:
            - Network issues: Will fail if model not cached and no internet
            - Memory issues: Large models may cause OOM on low-memory systems
            - Model not found: Invalid model names will cause runtime errors
            """
            return HuggingFaceEmbeddings(model_name=settings.hf_model_name)
    
    def get_qdrant_client(self,settings: Settings) -> QdrantClient:

        return QdrantClient(url=settings.qdrant_url)
    
    def upsert_chunks(self,client: QdrantClient, settings: Settings, chunks: List[Document], embeddings: HuggingFaceEmbeddings):
        vecs = embeddings.embed_documents([c.page_content for c in chunks])
        points = self.build_points(chunks, vecs)
        client.upsert(collection_name=settings.collection, points=points, wait=True)

    def build_points(self,chunks: List[Document], embeds: List[List[float]]) -> List[PointStruct]:
        pts: List[PointStruct] = []
        for i, (doc, vec) in enumerate(zip(chunks, embeds), start=1):
            payload = {
                "doc_id": doc.metadata.get("id"),
                "source": doc.metadata.get("source"),
                "title": doc.metadata.get("title"),
                "lang": doc.metadata.get("lang", "en"),
                "text": doc.page_content,
                "chunk_id": i - 1
            }
            pts.append(PointStruct(id=i, vector=vec, payload=payload))
        return pts
    
    def define_vector_db(self, settings: Settings, chunks):
        index = FAISS.from_documents(
            documents=chunks,
            #passare la funzione di embedding 
            embedding=self.embedder
        )
        return index
    
    def _create_documents(self) -> List[Document]:
        """Recupera dei bugiardini da cartella"""
        cartella = "rag\\input_docs"
        docs = []
        files = glob.glob(f"{cartella}/*.txt")
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                docs.append(Document(page_content=f.read(), metadata={"source": file}))
        return docs

    
    def split_docs(self):
        splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", ":", ";", " "]
        )
        docs = self._create_documents()
        chunks = splitter.split_documents(docs)
        return chunks
    
    def make_retriever(self,settings: Settings):
        """
        Configura il retriever. Con 'mmr' otteniamo risultati meno ridondanti e più coprenti.
        """
        if settings.search_type == "mmr":
            return self.vec_db.as_retriever(
                search_type="mmr",
                search_kwargs={"k": settings.k, "fetch_k": settings.fetch_k, "lambda_mult": settings.mmr_lambda},
            )
        else:
            return self.vec_db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.k},
            )
        
    def build_rag_chain(self):
        """
        Costruisce la catena RAG (retrieval -> prompt -> LLM) con citazioni e regole anti-hallucination.
        """
        template = (
            "Sei un medico esperto. Rispondi nella lingua della domanda. "
            "Usa esclusivamente il contenuto fornito all'interno del database   . "
            "Se l'informazione non è presente, dichiara che non è disponibile. "
            "Includi citazioni tra parentesi quadre nel formato [source:...]. "
            "Sii conciso, accurato e tecnicamente corretto       "
            "Contesto dal database: {context}"
            "Domanda: {question}"
            "Fornisci una risposta dettagliata, precisa e in italiano:"
        )

        prompt = ChatPromptTemplate.from_template(template)

        # LCEL: dict -> prompt -> llm -> parser
        chain = (
            {
                "context": RunnablePassthrough(), 
                "question": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain
    
    def rag_answer(self,question: str) -> str:
        """
        Esegue la catena RAG per una singola domanda.
        """
        return self.chain.invoke(question)
    
    
    

    
