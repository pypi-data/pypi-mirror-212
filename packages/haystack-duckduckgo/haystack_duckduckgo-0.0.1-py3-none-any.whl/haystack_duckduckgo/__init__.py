# SPDX-FileCopyrightText: 2023-present Lukas Kreussel <65088241+LLukas22@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

import json
import logging
from typing import Dict, List, Union, Optional, Any

from duckduckgo_search import DDGS
from haystack.nodes.search_engine.base import SearchEngine
from haystack import Document



class DuckDuckGoAPI(SearchEngine):
    def __init__(self,mode:str="search",backend:str="api",top_k: Optional[int] = 10,timeout:int=10,headers:Optional[Any]=None,proxies:Optional[Any]=None,search_engine_kwargs: Optional[Dict[str, Any]] = None) -> None:
        """
        :param mode: DuckDuckGo backend to use. "search" or "answer".
        :param backend: DuckDuckGo backend to use.
        :param top_k: Number of results to return.
        :param timeout: Timeout for the request to the DuckDuckGo API.
        :param headers: Headers to pass to the request to the DuckDuckGo API.
        :param proxies: Proxies to use for the request to the DuckDuckGo API.
        :param search_engine_kwargs: Additional parameters passed to the DuckDuckGo API.
        See the [duckduckgo-search documentation](https://github.com/deedy5/duckduckgo_search) for the full list of supported parameters.
        """
        super().__init__()
        self.backend = backend
        self.ddgs = DDGS(timeout=timeout,headers=headers,proxies=proxies)
        self.mode = mode
        self.top_k = top_k
        self.search_engine_kwargs = search_engine_kwargs if search_engine_kwargs else {}



    def search(self, query: str, **kwargs) -> List[Document]:
        """
        Search the search engine for the given query and return the results.
        :param query: The query to search for.
        :param kwargs: Additional parameters to pass to the search engine, such as top_k.
        :return: List of search results as documents.
        """
        kwargs = {**self.search_engine_kwargs, **kwargs}
        top_k = kwargs.pop("top_k", self.top_k)

        safe_search = kwargs.pop("safesearch", "moderate")
        region = kwargs.pop("region", "wt-wt")


        documents:List[Document] = []
        if self.mode == "answer":
            results = list(self.ddgs.answers(query))
            for result in results[:top_k]:
                documents.append(Document.from_dict({
                    "content": result["text"],
                    "title": result["url"].replace("https://duckduckgo.com/",""),
                    "link": result["url"],
                    "icon": result["icon"],
                }))
        else:
            results = list(self.ddgs.text(query, safesearch=safe_search, region=region, backend=self.backend))
            for result in results[:top_k]:
                documents.append(Document.from_dict({
                    "content": result["body"],
                    "title": result["title"],
                    "link": result["href"],
                }))
                

        return documents

