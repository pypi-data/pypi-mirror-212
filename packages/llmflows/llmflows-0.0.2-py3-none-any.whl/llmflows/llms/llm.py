# pylint: disable=too-few-public-methods

"""
This is the base module for all LLMs (Log-linear models).
Each specific LLM should extend this base class.
"""

from abc import ABC


class BaseLLM(ABC):
    """
    Base class for all Log-linear models (LLMs). Each specific LLM should extend this class.
    """

    def __init__(self, model):
        """
        Initializes the BaseLLM with a model.

        Args:
            model: The model for the LLM.
        """
        self.model = model
