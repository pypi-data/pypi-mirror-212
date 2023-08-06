from src.haystack_duckduckgo import DuckDuckGoAPI
from haystack import Document,MultiLabel
from typing import Optional,List,Dict,Tuple,Any,Union

def test_api_can_answer():
    api = DuckDuckGoAPI(mode="answer")
    documents = api.search("python")
    assert documents is not None
    assert len(documents) > 0
    assert type(documents[0]) == Document
    assert documents[0].content is not None
    assert documents[0].meta["title"] is not None
    assert documents[0].meta["link"] is not None

def test_api_can_search():
    api = DuckDuckGoAPI()
    documents = api.search("python")
    assert documents is not None
    assert len(documents) > 0
    assert type(documents[0]) == Document
    assert documents[0].content is not None
    assert documents[0].meta["title"] is not None
    assert documents[0].meta["link"] is not None

def test_works_with_websearch_node():
    from haystack.nodes.search_engine import WebSearch

    search_engine_provider = DuckDuckGoAPI()
    ws = WebSearch(api_key=None,search_engine_provider=search_engine_provider)
    results = ws.run(query="python")[0]
    assert results is not None

def test_works_with_webretriever_node():
    from haystack.nodes.retriever.web import WebRetriever
    from haystack import Pipeline

    search_engine_provider = DuckDuckGoAPI()
    wr = WebRetriever(api_key=None,search_engine_provider=search_engine_provider)
    p=Pipeline()
    p.add_node(wr,name="web_retriever",inputs=["Query"])
    results = p.run(query="python")
    assert results is not None
