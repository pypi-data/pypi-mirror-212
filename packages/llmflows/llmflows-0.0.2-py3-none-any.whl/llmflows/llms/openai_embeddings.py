# pylint: disable=too-few-public-methods

"""
This module helps with creating embeddings form OpenAIs API.
"""

import os
from typing import Union, List
import openai
from llmflows.vectorstores.vector_doc import VectorDoc
from .llm import BaseLLM



class OpenAIEmbeddings(BaseLLM):
    """
    A class for interacting with the OpenAI embeddings API.

    Args:
        model (str): The name of the OpenAI model to use.

    Attributes:
        api_key (str): The API key to use for authentication.
        model (str): The name of the OpenAI model to use.

    Methods:
        embed(
            docs: Union[VectorDoc, List[VectorDoc]]
        ) -> Union[VectorDoc, List[VectorDoc]]:
            Adds embeddings to a single or list of VectorDocs using OpenAI's service.
    """

    def __init__(self, model: str = "text-embedding-ada-002"):
        super().__init__(model)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    def embed(
        self, docs: Union[VectorDoc, List[VectorDoc]]
    ) -> Union[VectorDoc, List[VectorDoc]]:
        """
        Adds embeddings to a single or list of VectorDocs using OpenAI's service.

        Args:
            docs: A single VectorDoc or a list of VectorDocs to embed.

        Returns:
            If a single VectorDoc was passed, returns it with its embedding field
            updated.
            If a list of VectorDocs was passed, returns the list with the embedding
            field of each VectorDoc updated.
        """
        single_item = False

        if not isinstance(docs, list):  # if a single item was passed
            docs = [docs]
            single_item = True

        texts = [doc.doc for doc in docs]
        result = openai.Embedding.create(engine=self.model, input=texts)
        for i, doc in enumerate(docs):
            doc.embedding = result["data"][i]["embedding"]

        return docs[0] if single_item else docs
