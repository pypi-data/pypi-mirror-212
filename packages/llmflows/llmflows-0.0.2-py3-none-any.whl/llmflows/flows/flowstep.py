# pylint: disable=R0801, R0913

"""
This module contains the BaseFlowStep class which serves as a base class for
flow steps in a data processing pipeline.

This module defines the FlowStep class which is an implementation of a step 
in a data processing pipeline, based on the BaseFlowStep class.
"""

from typing import Dict, Any, List, Callable


class BaseFlowStep:
    """
    Base class for flow steps in a data processing pipeline.

    Attributes:
        name (str): The name of the flow step.
        output_key (str): The output key of the flow step.
        next_steps (List[BaseFlowStep]): Steps that this step connects to.
        parents (List[BaseFlowStep]): Steps that connect to this step.
    """

    def __init__(self, name: str, output_key: str):
        self.name = name
        self.output_key = output_key
        self.next_steps: List[BaseFlowStep] = []
        self.parents: List[BaseFlowStep] = []

    def execute(self, inputs):
        """
        Executes the flow step with given inputs.

        Args:
            inputs: Inputs to the flow step.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError

    def connect(self, *steps: "BaseFlowStep") -> None:
        """
        Connects this flow step to one or more other flow steps.

        Args:
            *steps (BaseFlowStep): Flow steps to connect to.

        Raises:
            ValueError: If connected flow steps have same output key.
        """
        self._check_unique_keys(*steps)

        self.next_steps.extend(steps)
        for step in steps:
            step.parents.append(self)

    def _check_unique_keys(self, *steps: "BaseFlowStep") -> None:
        """
        Checks if all connected flow steps have unique output keys.

        Args:
            *steps (BaseFlowStep): Flow steps to connect to.

        Raises:
            ValueError: If connected flow steps have same output key.
        """
        output_keys = [step.output_key for step in steps]
        if len(output_keys) != len(set(output_keys)):
            raise ValueError("All connected flowsteps must have unique output keys.")


class FlowStep(BaseFlowStep):
    """
    Represents a specific step in a Flow.

    Attributes:
        name (str): The name of the flow step.
        output_key (str): The key for the output of the flow step.
        llm: Language model to be used in the flow step.
        prompt_template: Template for the prompt to be used with the language model.
    """

    def __init__(
        self,
        name: str,
        llm: Any,
        prompt_template: Any,
        output_key: str,
        callbacks: List[Callable] = None,
    ):
        super().__init__(name, output_key)
        self.llm = llm
        self.prompt_template = prompt_template
        self.callbacks = callbacks if callbacks is not None else []

    def execute(self, inputs: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
        """
        Executes the flow step with provided inputs.

        Args:
            verbose: bool: Specifies if the flowstep should print its output
            inputs (Dict[str, Any]): Inputs to the flow step.

        Returns:
            Dict[str, Any]: Dictionary with the output key and the result.
        """
        prompt = self.prompt_template.get_prompt(**inputs)
        result = self.llm.generate(prompt)

        for callback in self.callbacks:
            if verbose:
                print(f"{self.name} Executing Callback: {callback.__name__}")
            callback(result)

        if verbose:
            print(f"{self.name}:\n{result}\n")

        return {self.output_key: result}
