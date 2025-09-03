import os
from typing import Type, List, Optional, Dict, Any

from crewai.tools import BaseTool
from langchain_openai import AzureOpenAIEmbeddings
from pydantic import BaseModel, Field, SecretStr
from contextlib import contextmanager
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import (
    SearchRequest, 
    ScoredPoint,
    VectorParams,
    Distance,
    Filter,
    FieldCondition,
    MatchValue
)


class RetrievalToolInput(BaseModel):
    """Input schema for RAGTool with Qdrant Hybrid Search parameters."""

    query: str = Field(..., description="The query to search in the vector store.")
    k: int = Field(default=5, description="Number of top similar documents to retrieve.")
    
    # Hybrid Search Parameters (from Qdrant documentation)
    top_n_semantic: int = Field(default=30, description="Quanti candidati prendere dalla ricerca semantica iniziale")
    top_n_text: int = Field(default=100, description="Massimo punti da considerare dal pre-filtro testuale")
    alpha: float = Field(default=0.75, description="Peso della componente semantica (0-1). 0.75 = priorità alla similarità vettoriale")
    text_boost: float = Field(default=0.3, description="Bonus additivo alle entry che matchano anche il testo (innalza la posizione in classifica)")
    final_k: int = Field(default=5, description="Quanti risultati finali vuoi dopo fusione e re-ranking")
    
    # MMR Parameters
    use_mmr: bool = Field(default=False, description="Se attivo, applica MMR ai top-N per diversificare")
    mmr_lambda: float = Field(default=0.6, description="MMR lambda (0=massima diversità, 1=massima rilevanza; tipico 0.5-0.7)")
    
    # Additional parameters
    score_threshold: float | None = Field(default=None, description="Minimum score threshold for retrieved documents.")
    consistency: int | None = Field(default=None, description="Consistency score for retrieved documents.")



def get_embedding_model() -> AzureOpenAIEmbeddings:
    """
    Restituisce il modello di embedding Azure OpenAI configurato via variabili d'ambiente.

    Parameters
    ----------
    None

    Returns
    -------
    AzureOpenAIEmbeddings
        Istanza configurata con `AZURE_API_BASE`, `AZURE_API_KEY`, `AZURE_API_VERSION`.

    Raises
    ------
    ValueError
        Se una tra `AZURE_API_BASE`, `AZURE_API_KEY`, `AZURE_API_VERSION` non è impostata.

    Notes
    -----
    Complessità temporale: O(1).
    Complessità spaziale: O(1).

    Examples
    --------
    >>> import os
    >>> from rag_or_web_flow.tools.rag_tool import get_embedding_model
    >>> saved = {k: os.environ.pop(k, None) for k in ("AZURE_API_BASE","AZURE_API_KEY","AZURE_API_VERSION")}
    >>> try:
    ...     get_embedding_model()
    ... except ValueError as e:
    ...     "AZURE_API_BASE" in str(e) or "AZURE_API_KEY" in str(e) or "AZURE_API_VERSION" in str(e)
    ... finally:
    ...     _ = [os.environ.__setitem__(k, v) for k, v in saved.items() if v is not None]
    True
    """
    endpoint_url = os.getenv("AZURE_API_BASE")
    api_key = os.getenv("AZURE_API_KEY")
    api_version = os.getenv("AZURE_API_VERSION")

    if not endpoint_url or not api_key or not api_version:
        raise ValueError(
            "Please set the AZURE_API_BASE, AZURE_API_KEY, and AZURE_API_VERSION environment variables."
        )

    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=endpoint_url,
        api_key=SecretStr(api_key),
        api_version=api_version,
        model="text-embedding-ada-002",
        chunk_size=1,
    )

    return embeddings


@contextmanager
def get_qdrant_client():
    """Context manager per ottenere un client Qdrant."""
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    client = QdrantClient(url=qdrant_url)
    
    try:
        yield client
    finally:
        client.close()


def calculate_mmr_scores(
    query_embedding: List[float], 
    candidates: List[ScoredPoint], 
    lambda_param: float = 0.6
) -> List[ScoredPoint]:
    """
    Implementa Maximum Marginal Relevance (MMR) per diversificare i risultati.
    
    Parameters
    ----------
    query_embedding : List[float]
        Embedding della query originale
    candidates : List[ScoredPoint]
        Lista dei candidati da riordinare
    lambda_param : float
        Parametro lambda per bilanciare rilevanza vs diversità (0-1)
        
    Returns
    -------
    List[ScoredPoint]
        Lista riordinata secondo MMR
    """
    if not candidates:
        return candidates
        
    selected = []
    remaining = candidates.copy()
    
    # Seleziona il primo elemento (più rilevante)
    if remaining:
        best = max(remaining, key=lambda x: x.score)
        selected.append(best)
        remaining.remove(best)
    
    # Seleziona iterativamente gli elementi rimanenti
    while remaining and len(selected) < len(candidates):
        mmr_scores = []
        
        for candidate in remaining:
            # Calcola similarità con la query (rilevanza)
            relevance_score = candidate.score
            
            # Calcola massima similarità con elementi già selezionati (ridondanza)
            max_similarity = 0
            
            # Estrai il vettore dal candidato
            candidate_vector = None
            if hasattr(candidate, 'vector') and candidate.vector is not None:
                if isinstance(candidate.vector, dict):
                    # Qdrant può restituire un dict con nome del vettore come chiave
                    # Prendiamo il primo vettore disponibile
                    candidate_vector = list(candidate.vector.values())[0]
                elif isinstance(candidate.vector, list):
                    candidate_vector = candidate.vector
                else:
                    # Potrebbe essere un oggetto vector wrapper
                    candidate_vector = getattr(candidate.vector, 'vector', None)
            
            if candidate_vector and isinstance(candidate_vector, list):
                for selected_item in selected:
                    # Estrai il vettore dall'elemento selezionato
                    selected_vector = None
                    if hasattr(selected_item, 'vector') and selected_item.vector is not None:
                        if isinstance(selected_item.vector, dict):
                            selected_vector = list(selected_item.vector.values())[0]
                        elif isinstance(selected_item.vector, list):
                            selected_vector = selected_item.vector
                        else:
                            selected_vector = getattr(selected_item.vector, 'vector', None)
                    
                    if selected_vector and isinstance(selected_vector, list):
                        try:
                            # Cosine similarity
                            candidate_array = np.array(candidate_vector)
                            selected_array = np.array(selected_vector)
                            
                            dot_product = np.dot(candidate_array, selected_array)
                            norm_candidate = np.linalg.norm(candidate_array)
                            norm_selected = np.linalg.norm(selected_array)
                            
                            if norm_candidate > 0 and norm_selected > 0:
                                similarity = dot_product / (norm_candidate * norm_selected)
                                max_similarity = max(max_similarity, similarity)
                        except Exception:
                            # Se il calcolo della similarità fallisce, ignora
                            pass
            
            # Calcola MMR score
            mmr_score = lambda_param * relevance_score - (1 - lambda_param) * max_similarity
            mmr_scores.append((candidate, mmr_score))
        
        # Seleziona l'elemento con MMR score più alto
        if mmr_scores:
            best_candidate, _ = max(mmr_scores, key=lambda x: x[1])
            selected.append(best_candidate)
            remaining.remove(best_candidate)
        else:
            break
    
    return selected


def perform_hybrid_search(
    client: QdrantClient,
    collection_name: str,
    query_text: str,
    query_embedding: List[float],
    top_n_semantic: int = 30,
    top_n_text: int = 100,
    alpha: float = 0.75,
    text_boost: float = 0.3,
    final_k: int = 5,
    score_threshold: Optional[float] = None
) -> List[ScoredPoint]:
    """
    Implementa Hybrid Search combinando ricerca semantica e testuale.
    
    Parameters
    ----------
    client : QdrantClient
        Client Qdrant
    collection_name : str
        Nome della collezione
    query_text : str
        Testo della query per la ricerca testuale
    query_embedding : List[float]
        Embedding della query per la ricerca semantica
    top_n_semantic : int
        Numero di candidati dalla ricerca semantica
    top_n_text : int
        Numero di candidati dalla ricerca testuale
    alpha : float
        Peso della componente semantica (0-1)
    text_boost : float
        Boost per documenti che matchano anche il testo
    final_k : int
        Numero di risultati finali
    score_threshold : Optional[float]
        Soglia minima di score
        
    Returns
    -------
    List[ScoredPoint]
        Risultati dell'hybrid search
    """
    # 1. Ricerca semantica (vettoriale)
    semantic_results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_n_semantic,
        score_threshold=score_threshold,
        with_payload=True,
        with_vectors=True
    )
    
    # 2. Ricerca testuale (se supportata dalla collezione)
    # Nota: questo è un'implementazione semplificata
    # In una implementazione reale, useresti il full-text search di Qdrant
    text_results = []
    try:
        # Simulazione di ricerca testuale usando filtri sui metadati
        # In produzione, useresti qdrant text search capabilities
        text_filter = Filter(
            must=[
                FieldCondition(
                    key="text",
                    match=MatchValue(value=query_text)
                )
            ]
        )
        
        text_results = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,  # Usiamo comunque l'embedding per ordinare
            query_filter=text_filter,
            limit=top_n_text,
            with_payload=True,
            with_vectors=True
        )
    except Exception:
        # Se la ricerca testuale fallisce, usiamo solo quella semantica
        text_results = []
    
    # 3. Fusione e re-ranking
    # Combina i risultati usando gli ID per evitare duplicati
    all_results = {}
    
    # Aggiungi risultati semantici
    for result in semantic_results:
        result_id = result.id
        semantic_score = result.score
        all_results[result_id] = {
            'point': result,
            'semantic_score': semantic_score,
            'text_match': False
        }
    
    # Aggiungi boost per risultati che matchano anche il testo
    text_ids = {result.id for result in text_results}
    for result_id in all_results:
        if result_id in text_ids:
            all_results[result_id]['text_match'] = True
    
    # 4. Calcola score finale
    final_results = []
    for result_id, data in all_results.items():
        semantic_score = data['semantic_score']
        text_match_boost = text_boost if data['text_match'] else 0
        
        # Formula hybrid score: alpha * semantic_score + text_boost (se match testuale)
        final_score = alpha * semantic_score + text_match_boost
        
        # Aggiorna lo score del punto
        point = data['point']
        point.score = final_score
        final_results.append(point)
    
    # 5. Ordina per score finale e prendi i top final_k
    final_results.sort(key=lambda x: x.score, reverse=True)
    return final_results[:final_k]


class RetrievalTool(BaseTool):
    name: str = "Hybrid Retrieval Tool"
    description: str = "Advanced tool that retrieves relevant information from Qdrant using hybrid search combining semantic and text-based search with configurable parameters."
    args_schema: Type[BaseModel] = RetrievalToolInput

    def _run(
        self, 
        query: str, 
        k: int = 5,
        top_n_semantic: int = 30,
        top_n_text: int = 100,
        alpha: float = 0.75,
        text_boost: float = 0.3,
        final_k: int = 5,
        use_mmr: bool = False,
        mmr_lambda: float = 0.6,
        score_threshold: float | None = None,
        consistency: int | None = None
    ) -> str:
        """
        Esegue una ricerca ibrida (semantica + testuale) su Qdrant con parametri configurabili.

        Parameters
        ----------
        query : str
            Query da cercare nella collezione Qdrant.
        k : int
            Numero di documenti da restituire (deprecato, usa final_k).
        top_n_semantic : int
            Numero di candidati dalla ricerca semantica iniziale.
        top_n_text : int
            Numero massimo di punti da considerare dal pre-filtro testuale.
        alpha : float
            Peso della componente semantica (0-1). 0.75 = priorità alla similarità vettoriale.
        text_boost : float
            Bonus additivo per documenti che matchano anche il testo.
        final_k : int
            Numero di risultati finali dopo fusione e re-ranking.
        use_mmr : bool
            Se True, applica MMR per diversificare i risultati.
        mmr_lambda : float
            Parametro lambda per MMR (0=massima diversità, 1=massima rilevanza).
        score_threshold : float | None
            Soglia minima di score per i documenti recuperati.
        consistency : int | None
            Parametro di consistenza per Qdrant (non implementato).

        Returns
        -------
        str
            Concatenazione dei contenuti dei documenti trovati, separati da "---".

        Raises
        ------
        ValueError
            Se `query` è vuota o composta solo da spazi.
        ValueError
            Se le variabili d'ambiente richieste non sono impostate.

        Notes
        -----
        Implementa l'Hybrid Search di Qdrant seguendo i parametri dell'immagine fornita:
        - top_n_semantic: candidati dalla ricerca semantica
        - top_n_text: punti dal pre-filtro testuale  
        - alpha: peso componente semantica
        - text_boost: bonus per match testuali
        - final_k: risultati finali
        - MMR opzionale per diversificazione
        
        Consiglio pratico: inizia con alpha=0.7-0.85 e text_boost=0.15-0.3,
        poi calibra su un set di domande/risposte atteso.
        """
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string.")

        # Usa final_k invece di k per coerenza con i parametri hybrid search
        if final_k <= 0:
            final_k = k if k > 0 else 5

        # Ottieni l'embedding della query
        embeddings = get_embedding_model()
        query_embedding = embeddings.embed_query(query)

        with get_qdrant_client() as client:
            # Ottieni il nome della collezione (configurabile via env)
            collection_name = os.getenv("QDRANT_COLLECTION_NAME", "minecraft_kb")
            
            # Esegui hybrid search
            results = perform_hybrid_search(
                client=client,
                collection_name=collection_name,
                query_text=query,
                query_embedding=query_embedding,
                top_n_semantic=top_n_semantic,
                top_n_text=top_n_text,
                alpha=alpha,
                text_boost=text_boost,
                final_k=final_k,
                score_threshold=score_threshold
            )

            # Applica MMR se richiesto
            if use_mmr and len(results) > 1:
                results = calculate_mmr_scores(
                    query_embedding=query_embedding,
                    candidates=results,
                    lambda_param=mmr_lambda
                )

        # Estrai il contenuto dai risultati
        result_contents = []
        for result in results:
            # Ottieni il contenuto dal payload
            if result.payload and 'page_content' in result.payload:
                content = result.payload['page_content']
            elif result.payload and 'text' in result.payload:
                content = result.payload['text']
            elif result.payload and 'content' in result.payload:
                content = result.payload['content']
            else:
                # Fallback: converti tutto il payload in stringa
                content = str(result.payload) if result.payload else f"Document ID: {result.id}"
            
            # Aggiungi informazioni di score se utili per debug
            content_with_score = f"[Score: {result.score:.4f}] {content}"
            result_contents.append(content_with_score)

        # Unisci i contenuti
        result_str = "\n---\n".join(result_contents)
        
        return result_str


