# haystack-duckduckgo

[![PyPI - Version](https://img.shields.io/pypi/v/haystack-duckduckgo.svg)](https://pypi.org/project/haystack-duckduckgo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/haystack-duckduckgo.svg)](https://pypi.org/project/haystack-duckduckgo)

Use the [DuckDuckGo](https://duckduckgo.com/) search engine with your haystack pipeline or agents.
-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install haystack-duckduckgo
```
## Usage
This package allows you to use the [DuckDuckGo](https://duckduckgo.com/) search api, which does not require an API key and can be used free of charge.

Use it in Haystacks [WebSearch](https://docs.haystack.deepset.ai/docs/search_engine#websearch) component:
```python
from haystack_duckduckgo import DuckDuckGoAPI
from haystack.nodes.search_engine import WebSearch

#Build the DuckDuckGo provider
search_engine_provider = DuckDuckGoAPI()
#Initialize the `WebSearch` node with the provider
ws = WebSearch(api_key=None,search_engine_provider=search_engine_provider)

#Use the `WebSearch` node
results = ws.run(query="python programming language")[0]
print(results)
```

Use it in a Haystack [WebRetriever](https://docs.haystack.deepset.ai/reference/retriever-api#webretriever)

```python
from haystack_duckduckgo import DuckDuckGoAPI
from haystack.nodes.retriever.web import WebRetriever
from haystack import Pipeline

#Build the DuckDuckGo provider
search_engine_provider = DuckDuckGoAPI()

#Build the pipeline
wr = WebRetriever(api_key=None,search_engine_provider=search_engine_provider)
p=Pipeline()
p.add_node(wr,name="web_retriever",inputs=["Query"])

#Run the pipeline
results = p.run(query="python")
print(results)
```
## License

`haystack-duckduckgo` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
