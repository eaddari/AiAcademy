from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Any, Iterable, Tuple

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# LangChain Core components for prompt/chain construction
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import init_chat_model

# Qdrant vector database client and models
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

    qdrant_url: str = "http://localhost:6333"
    collection: str = "rag_chunks"
    chunk_size: int = 500
    chunk_overlap: int = 200
    top_n_semantic: int = 50
    top_n_text: int = 130
    final_k: int = 8
    alpha: float = 0.75
    text_boost: float = 0.20
    use_mmr: bool = True
    mmr_lambda: float = 0.6
    lm_base_env: str = "OPENAI_BASE_URL"
    lm_key_env: str = "OPENAI_API_KEY"
    lm_model_env: str = "LMSTUDIO_MODEL"
SETTINGS = Settings()

def get_embeddings(self) -> AzureOpenAIEmbeddings:
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_API_BASE"),
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION"),
        model="text-embedding-ada-002"
    )
def get_llm(settings: Settings):
    try:
        # Check for Azure OpenAI configuration first
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_API_BASE")
        azure_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_API_KEY")
        azure_version = os.getenv("AZURE_OPENAI_API_VERSION") or os.getenv("AZURE_API_VERSION")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if not deployment_name:
            model_env = os.getenv("LMSTUDIO_MODEL") or os.getenv("MODEL")
            if model_env and "/" in model_env:
                deployment_name = model_env.split("/", 1)[1]
            else:
                deployment_name = model_env
        
        if azure_endpoint and azure_key and azure_version and deployment_name:
            print("Configuring Azure OpenAI...")
            # Use Azure OpenAI - use deployment name without prefix
            llm = init_chat_model(
                model=deployment_name,  # Just "gpt-4.1", not "azure/gpt-4.1"
                model_provider="azure_openai",
                azure_endpoint=azure_endpoint,
                api_key=azure_key,
                api_version=azure_version
            )
            # Simple test to verify the LLM works
            try:
                test_response = llm.invoke("test")
                if test_response:
                    print("Azure OpenAI configured successfully")
                    return llm
                else:
                    print("Azure OpenAI test failed - skipping generation step")
                    return None
            except Exception as e:
                print(f"LLM configuration error: {e}")
                print("Continuing without LLM - will show retrieved content only")
                return None

        base = os.getenv("OPENAI_BASE_URL")
        key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("LMSTUDIO_MODEL")

        if not (base and key and model_name):
            print("LLM not configured - skipping generation step")
            return None
            
        # Test the LLM connection before returning
        try:
            llm = init_chat_model(model_name, model_provider="openai")
            # Simple test to verify the LLM works
            test_response = llm.invoke("test")
            if test_response:
                print("LLM configured successfully")
                return llm
            else:
                print("LLM test failed - skipping generation step")
                return None
        except Exception as e:
            print(f"LLM configuration error: {e}")
            print("LLM test failed - skipping generation step")
            return None

    except Exception as e:
        print(f"LLM configuration error: {e}")
        print("Continuing without LLM - will show retrieved content only")
        return None
            
    except Exception as e:
        print(f"LLM configuration error: {e}")
        print("Continuing without LLM - will show retrieved content only")
        return None

def simulate_corpus() -> List[Document]:
    docs = []
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    input_docs_path = script_dir / "input_docs"
    
    for file_path in input_docs_path.glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                docs.append(Document(page_content=content, metadata={"source": file_path.name}))
    return docs

def split_documents(docs: List[Document], settings: Settings) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ": ", ", ", " ", ""],
    )
    return splitter.split_documents(docs)

def get_qdrant_client(settings: Settings) -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)

def recreate_collection_for_rag(client: QdrantClient, settings: Settings, vector_size: int):

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

def build_points(chunks: List[Document], embeds: List[List[float]]) -> List[PointStruct]:
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

def upsert_chunks(client: QdrantClient, settings: Settings, chunks: List[Document], embeddings: AzureOpenAIEmbeddings):
    vecs = embeddings.embed_documents([c.page_content for c in chunks])
    points = build_points(chunks, vecs)
    client.upsert(collection_name=settings.collection, points=points, wait=True)

def qdrant_semantic_search(
    client: QdrantClient,
    settings: Settings,
    query: str,
    embeddings: AzureOpenAIEmbeddings,
    limit: int,
    with_vectors: bool = False
):
    qv = embeddings.embed_query(query)
    res = client.query_points(
        collection_name=settings.collection,
        query=qv,
        limit=limit,
        with_payload=True,
        with_vectors=with_vectors,
        search_params=SearchParams(
            hnsw_ef=256,  # ampiezza lista in fase di ricerca (recall/latency)
            exact=False   # True = ricerca esatta (lenta); False = ANN HNSW
        ),
    )
    return res.points

def qdrant_text_prefilter_ids(
    client: QdrantClient,
    settings: Settings,
    query: str,
    max_hits: int
) -> List[int]:

    matched_ids: List[int] = []
    next_page = None
    while True:
        points, next_page = client.scroll(
            collection_name=settings.collection,
            scroll_filter=Filter(
                must=[FieldCondition(key="text", match=MatchText(text=query))]
            ),
            limit=min(256, max_hits - len(matched_ids)),
            offset=next_page,
            with_payload=False,
            with_vectors=False,
        )
        matched_ids.extend([p.id for p in points])
        if not next_page or len(matched_ids) >= max_hits:
            break
    return matched_ids

def mmr_select(
    query_vec: List[float],
    candidates_vecs: List[List[float]],
    k: int,
    lambda_mult: float
) -> List[int]:

    import numpy as np
    V = np.array(candidates_vecs, dtype=float)
    q = np.array(query_vec, dtype=float)

    def cos(a, b):
        na = (a @ a) ** 0.5 + 1e-12
        nb = (b @ b) ** 0.5 + 1e-12
        return float((a @ b) / (na * nb))

    sims = [cos(v, q) for v in V]
    selected: List[int] = []
    remaining = set(range(len(V)))

    while len(selected) < min(k, len(V)):
        if not selected:
            # pick the highest similarity first
            best = max(remaining, key=lambda i: sims[i])
            selected.append(best)
            remaining.remove(best)
            continue
        best_idx = None
        best_score = -1e9
        for i in remaining:
            max_div = max([cos(V[i], V[j]) for j in selected]) if selected else 0.0
            score = lambda_mult * sims[i] - (1 - lambda_mult) * max_div
            if score > best_score:
                best_score = score
                best_idx = i
        selected.append(best_idx)
        remaining.remove(best_idx)
    return selected

def hybrid_search(
    client: QdrantClient,
    settings: Settings,
    query: str,
    embeddings: AzureOpenAIEmbeddings
):
    
    sem = qdrant_semantic_search(
        client, settings, query, embeddings,
        limit=settings.top_n_semantic, with_vectors=True
    )
    if not sem:
        return []

    # (2) full-text prefilter (id)
    text_ids = set(qdrant_text_prefilter_ids(client, settings, query, settings.top_n_text))

    # Normalizzazione score semantici per fusione
    scores = [p.score for p in sem]
    smin, smax = min(scores), max(scores)
    def norm(x):  # robusto al caso smin==smax
        return 1.0 if smax == smin else (x - smin) / (smax - smin)

    # (3) fusione con boost testuale
    fused: List[Tuple[int, float, Any]] = []  # (idx, fused_score, point)
    for idx, p in enumerate(sem):
        base = norm(p.score)                    # [0..1]
        fuse = settings.alpha * base
        if p.id in text_ids:
            fuse += settings.text_boost         # boost additivo
        fused.append((idx, fuse, p))

    # ordina per fused_score desc
    fused.sort(key=lambda t: t[1], reverse=True)

    # MMR opzionale per diversificare i top-K
    if settings.use_mmr:
        qv = embeddings.embed_query(query)
        # prendiamo i primi N dopo fusione (es. 30) e poi MMR per final_k
        N = min(len(fused), max(settings.final_k * 5, settings.final_k))
        cut = fused[:N]
        vecs = [sem[i].vector for i, _, _ in cut]
        mmr_idx = mmr_select(qv, vecs, settings.final_k, settings.mmr_lambda)
        picked = [cut[i][2] for i in mmr_idx]
        return picked

    # altrimenti, prendi i primi final_k dopo fusione
    return [p for _, _, p in fused[:settings.final_k]]


def format_docs_for_prompt(points: Iterable[Any]) -> str:
    blocks = []
    for p in points:
        pay = p.payload or {}
        src = pay.get("source", "unknown")
        blocks.append(f"[source:{src}] {pay.get('text','')}")
    return "\n\n".join(blocks)

def build_rag_chain(llm):
    system_prompt = (
        "You are a technical assistant. Answer in English, concisely and accurately. "
        "Use EXCLUSIVELY the information present in the CONTENT. "
        "If information is not present, state: 'Information not available in the provided context.' "
        "Always cite sources in the format [source:FILE]."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human",
         "Question:\n{question}\n\n"
         "CONTENT:\n{context}\n\n"
         "Instructions:\n"
         "1) Answer based only on the content.\n"
         "2) Include citations [source:...].\n"
         "3) No fabrications.")
    ])

    chain = (
        {
            "context": RunnablePassthrough(),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain