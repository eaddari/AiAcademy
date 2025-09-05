import arxiv
from typing import List, Dict, Any
from crewai.tools import tool

@tool("ArXiv Searcher")
def arxiv_searcher_tool(arxiv_queries: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    ArXiv Searcher Tool
    Performs a search on arXiv for a list of queries and returns links to the found papers.

    Parameters
    ----------
    arxiv_queries : List[str]
        A list of search strings to query the arXiv database.

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
        A dictionary where each key is a query string and the value is a list of papers found.
        Each paper is represented as a dictionary with title, authors, abstract, year, and link.

    Notes
    -----
    If an error occurs during the search of a specific query, that query will have an empty list.
    """
    results: Dict[str, List[Dict[str, Any]]] = {}
    client = arxiv.Client()

    for query in arxiv_queries:
        try:
            search = arxiv.Search(
                query=query,
                max_results=1,
                sort_by=arxiv.SortCriterion.Relevance
            )

            papers = []
            for paper in client.results(search):
                info_paper = {
                    "title": paper.title,
                    "authors": ", ".join(author.name for author in paper.authors),
                    "abstract": paper.summary.strip().replace("\n", " "),
                    "year": paper.published.year,
                    "link": paper.entry_id
                }
                papers.append(info_paper)

            results[query] = papers
            print(f"Found {len(papers)} papers for the query: '{query}'")

        except Exception as e:
            print(f"Error during search for query '{query}': {e}")
            results[query] = []

    return results
