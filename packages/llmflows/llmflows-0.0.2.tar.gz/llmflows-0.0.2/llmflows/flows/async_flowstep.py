# pylint: disable=R0801, R0913

"""
This module provides async flow step classes: AsyncBaseFlowStep and AsyncFlowStep.
These steps form the fundamental units in an AsyncFlow, allowing async processing.
"""

from typing import List, Dict, Any, Callable


class AsyncBaseFlowStep:
    """Base class for all asynchronous flow steps."""

    def __init__(self, name: str, output_key: str):
        """
        Initializes the AsyncBaseFlowStep.

        Args:
            name (str): The name of the flow step.
            output_key (str): The unique output key of the flow step.
        """
        self.name = name
        self.output_key = output_key
        self.next_steps: List[AsyncBaseFlowStep] = []
        self.parents: List[AsyncBaseFlowStep] = []

    async def execute(self, inputs: Dict[str, Any]):
        """
        Placeholder for step execution method. To be overridden in subclasses.

        Args:
            inputs (Dict[str, Any]): Inputs to the step.

        Raises:
            NotImplementedError: If not implemented in subclass.
        """
        raise NotImplementedError

    def connect(self, *steps: "AsyncBaseFlowStep") -> None:
        """
        Connects current step to next steps in the flow.

        Args:
            *steps (AsyncBaseFlowStep): Next steps to connect to.

        Raises:
            ValueError: If connected flow steps have duplicate output keys.
        """
        self._check_unique_keys(*steps)
        self.next_steps.extend(steps)
        for step in steps:
            step.parents.append(self)

    def _check_unique_keys(self, *steps: "AsyncBaseFlowStep") -> None:
        """
        Ensures unique output keys among connected steps.

        Args:
            *steps (AsyncBaseFlowStep): Steps to check.

        Raises:
            ValueError: If duplicate output keys exist.
        """
        output_keys = [step.output_key for step in steps]
        if len(output_keys) != len(set(output_keys)):
            raise ValueError("All connected flowsteps must have unique output keys.")


class AsyncFlowStep(AsyncBaseFlowStep):
    """A specific implementation of asynchronous flow step."""

    def __init__(
        self,
        name: str,
        llm: Any,
        prompt_template: Any,
        output_key: str,
        callbacks: List[Callable] = None,
    ):
        """
        Initializes the AsyncFlowStep.

        Args:
            name (str): The name of the flow step.
            llm (Any): The language model used for generation.
            prompt_template (Any): Template for generating the prompt.
            output_key (str): The unique output key of the flow step.
        """
        super().__init__(name, output_key)
        self.llm = llm
        self.prompt_template = prompt_template
        self.callbacks = callbacks if callbacks else []

    async def execute(
        self, inputs: Dict[str, Any], verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Executes the flow step asynchronously.

        Args:
            inputs (Dict[str, Any]): Inputs to the step.
            verbose (bool): If true, step output is printed.

        Returns:
            Dict[str, Any]: Output of the step, with output_key as the key.
        """
        print(f"Flowstep {self.name} started")
        prompt = self.prompt_template.get_prompt(**inputs)
        result = await self.llm.generate_async(prompt)

        for callback in self.callbacks:
            if verbose:
                print(f"{self.name} Executing Callback: {callback.__name__}")
            callback(result)

        if verbose:
            print(f"{self.name}:\n{result}\n")

        return {self.output_key: result}
